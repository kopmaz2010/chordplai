-- ═══════════════════════════════════════════════════════════════
--  ACİL GÜVENLİK DÜZELTMESİ — ChordPlai · 31 Temmuz 2026
--  Tamamını kopyala → yapıştır → Run. Tek seferde her şeyi kapatır.
--
--  Panel: https://supabase.com/dashboard/project/cnpfhcjxxtboylvvqbfz/sql/new
--
--  SORUN: profiles tablosundaki politika "for select using (true)" idi.
--  anon anahtarı sitede herkese açık olduğu için (bu normaldir, koruma
--  RLS'ten gelir) internetteki HERKES tek istekle bütün üye listesini
--  çekebiliyordu: 553 kayıt, ad + avatar + E-POSTA.
--
--  KÖK NEDEN: RLS satır bazlıdır, sütun bazlı DEĞİLDİR. Liderlik tablosu
--  için takma adı herkese açmak istenmiş; aynı politika e-postayı da açmış.
-- ═══════════════════════════════════════════════════════════════

begin;

-- ── 1) Okuma yetkisini kendi satırına kilitle ────────────────────
drop policy if exists "profiles_public_read" on public.profiles;
drop policy if exists "profiles_own_read"    on public.profiles;
create policy "profiles_own_read" on public.profiles
  for select using (auth.uid() = id);

-- ── 2) Herkese açık alanlar AYRI görünümde (e-posta YOK) ─────────
-- Liderlik tablosu ve profil kartı bunu kullanacak. Sütunlar burada
-- tek tek yazılıdır; profiles'a yeni sütun eklersen buraya EKLEME.
create or replace view public.public_profiles as
  select id, display_name, avatar_url from public.profiles;
grant select on public.public_profiles to anon, authenticated;

-- ── 3) VERİ MİNİMİZASYONU: e-postayı profiles'ta hiç tutma ───────
-- Uygulama profiles.email'i HİÇ okumuyor (arayüzdeki e-posta oturumdan
-- geliyor). Gerçek kopyası auth.users tablosunda duruyor ve orası REST
-- ile dışarı açık değil. İkinci bir kopya yalnızca risk demek.
-- KVKK'nın veri minimizasyonu ilkesi de bunu gerektiriyor.

-- 3a) Yeni kayıtlarda e-posta yazan tetikleyiciyi güncelle
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, display_name, avatar_url)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'name', split_part(coalesce(new.email, 'oyuncu'), '@', 1)),
    new.raw_user_meta_data->>'avatar_url'
  )
  on conflict (id) do nothing;
  return new;
end $$;

-- 3b) Mevcut 553 kaydın e-postasını temizle
update public.profiles set email = null where email is not null;

-- 3c) Sütunu tamamen kaldır (geri almak istersen bu satırı yorum yap)
alter table public.profiles drop column if exists email;

commit;

-- ═══════════════════════════════════════════════════════════════
--  DOĞRULAMA — çalıştırdıktan sonra terminalde:
--
--    cd ~/akor-antrenoru
--    ANON=$(grep -o 'anon: *"[^"]*"' index.html | head -1 | sed 's/.*"\(.*\)"/\1/')
--    BASE=https://cnpfhcjxxtboylvvqbfz.supabase.co
--
--    # 1) Artık BOŞ dizi [] dönmeli — sızıntı kapandı:
--    curl -s "$BASE/rest/v1/profiles?select=*&limit=5" -H "apikey: $ANON"
--
--    # 2) Takma adlar dönmeli — liderlik tablosu çalışmaya devam ediyor:
--    curl -s "$BASE/rest/v1/public_profiles?select=display_name&limit=5" -H "apikey: $ANON"
--
--    # 3) Üye sayacı bozulmamalı (security definer, etkilenmez):
--    curl -s -X POST "$BASE/rest/v1/rpc/user_count" -H "apikey: $ANON" \
--         -H "Content-Type: application/json" -d '{}'
--
--  Sonra bana "çalıştırdım" de, üçünü de ben doğrulayayım.
-- ═══════════════════════════════════════════════════════════════
