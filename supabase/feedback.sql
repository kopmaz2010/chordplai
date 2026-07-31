-- ═══════════════════════════════════════════════════════════════
--  ChordPlai — Geri Bildirim Sistemi + BEKLEYEN GÜVENLİK DÜZELTMESİ
--  Tamamını kopyala → yapıştır → Run. İkisini birden halleder.
--
--  Panel: https://supabase.com/dashboard/project/cnpfhcjxxtboylvvqbfz/sql/new
-- ═══════════════════════════════════════════════════════════════

begin;

-- ───────────────────────────────────────────────────────────────
-- BÖLÜM 1 — BEKLEYEN GÜVENLİK DÜZELTMESİ (599 e-posta sızıntısı)
-- profiles'taki "for select using (true)" politikası herkesin tüm
-- üye listesini (ad + avatar + E-POSTA) çekmesine izin veriyordu.
-- Veri silmez; yalnızca okuma yetkisini kendi satırına kilitler.
-- ───────────────────────────────────────────────────────────────
drop policy if exists "profiles_public_read" on public.profiles;
drop policy if exists "profiles_own_read"    on public.profiles;
create policy "profiles_own_read" on public.profiles
  for select using (auth.uid() = id);

-- Liderlik tablosu/profil kartı için e-postasız görünüm
create or replace view public.public_profiles as
  select id, display_name, avatar_url from public.profiles;
grant select on public.public_profiles to anon, authenticated;

-- ───────────────────────────────────────────────────────────────
-- BÖLÜM 2 — YÖNETİCİ TANIMI
-- ───────────────────────────────────────────────────────────────
create or replace function public.is_admin()
returns boolean
language sql stable security definer set search_path = public
as $$
  select coalesce(auth.jwt() ->> 'email', '') = 'kopmaz2010@gmail.com'
$$;
grant execute on function public.is_admin() to anon, authenticated;

-- ───────────────────────────────────────────────────────────────
-- BÖLÜM 3 — GERİ BİLDİRİM TABLOSU
-- ───────────────────────────────────────────────────────────────
create table if not exists public.feedback (
  id         bigint generated always as identity primary key,
  user_id    uuid references auth.users(id) on delete set null,  -- giriş yapmadıysa null
  kind       text not null check (kind in ('istek','oneri','sikayet')),
  message    text not null check (char_length(message) between 5 and 2000),
  contact    text check (contact is null or char_length(contact) <= 120),
  page       text,          -- hangi bölümden gönderildi
  lang       text,
  status     text not null default 'yeni' check (status in ('yeni','okundu','yapiliyor','tamam','kapali')),
  admin_note text,
  created_at timestamptz not null default now()
);

create index if not exists feedback_created_idx on public.feedback (created_at desc);
create index if not exists feedback_status_idx  on public.feedback (status);

alter table public.feedback enable row level security;

-- HERKES gönderebilir (giriş şart değil — fikir duymak istiyoruz).
-- user_id ya kendi kimliğin olmalı ya da boş; başkasının adına yazılamaz.
drop policy if exists "feedback_insert_any" on public.feedback;
create policy "feedback_insert_any" on public.feedback
  for insert with check (user_id is null or user_id = auth.uid());

-- Kendi gönderdiğini görebilirsin; yönetici hepsini görür.
drop policy if exists "feedback_read_own_or_admin" on public.feedback;
create policy "feedback_read_own_or_admin" on public.feedback
  for select using (user_id = auth.uid() or public.is_admin());

-- Yalnız yönetici durum/not güncelleyebilir.
drop policy if exists "feedback_admin_update" on public.feedback;
create policy "feedback_admin_update" on public.feedback
  for update using (public.is_admin()) with check (public.is_admin());

-- Yalnız yönetici silebilir (spam temizliği).
drop policy if exists "feedback_admin_delete" on public.feedback;
create policy "feedback_admin_delete" on public.feedback
  for delete using (public.is_admin());

-- ───────────────────────────────────────────────────────────────
-- BÖLÜM 4 — YÖNETİCİ ÖZETİ (panel rozetleri için)
-- ───────────────────────────────────────────────────────────────
create or replace function public.feedback_stats()
returns json
language sql stable security definer set search_path = public
as $$
  select case when public.is_admin() then (
    select json_build_object(
      'toplam',   count(*),
      'yeni',     count(*) filter (where status = 'yeni'),
      'istek',    count(*) filter (where kind = 'istek'),
      'oneri',    count(*) filter (where kind = 'oneri'),
      'sikayet',  count(*) filter (where kind = 'sikayet')
    ) from public.feedback
  ) else null end
$$;
grant execute on function public.feedback_stats() to authenticated;

commit;

-- ═══════════════════════════════════════════════════════════════
--  DOĞRULAMA — terminalde:
--
--    cd ~/akor-antrenoru
--    ANON=$(grep -o 'anon: *"[^"]*"' index.html | head -1 | sed 's/.*"\(.*\)"/\1/')
--    BASE=https://cnpfhcjxxtboylvvqbfz.supabase.co
--
--    # 1) Sızıntı kapandı mı → [] dönmeli:
--    curl -s "$BASE/rest/v1/profiles?select=email&limit=5" -H "apikey: $ANON"
--
--    # 2) Takma adlar hâlâ okunabilir mi → dizi dönmeli:
--    curl -s "$BASE/rest/v1/public_profiles?select=display_name&limit=3" -H "apikey: $ANON"
--
--    # 3) Geri bildirim tablosu hazır mı → [] dönmeli (yetkisiz okuma yok):
--    curl -s "$BASE/rest/v1/feedback?select=id&limit=1" -H "apikey: $ANON"
-- ═══════════════════════════════════════════════════════════════
