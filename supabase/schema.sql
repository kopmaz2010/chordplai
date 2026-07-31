-- ChordPlai üyelik şeması
-- Supabase SQL Editor'de tek seferde çalıştır (SETUP-UYELIK.md'deki 3. adım).

-- 👤 Profiller: Google ile giren her kullanıcıya bir satır
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  avatar_url text,
  email text,
  instrument text default 'gitar',
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

-- ⚠️ GÜVENLİK: "for select using (true)" ile herkes TÜM satırları okuyabiliyordu.
-- RLS satır bazlıdır, sütun bazlı değildir — yani takma adı açmak istediğimizde
-- e-posta da açılıyordu. anon anahtarı sitede herkese açık olduğu için tüm
-- üyelerin e-postası dışarıdan listelenebiliyordu. Doğru kalıp: tabloyu kendi
-- satırına kilitle, herkese açık alanları AYRI BİR GÖRÜNÜMLE ver.
create policy "profiles_own_read" on public.profiles
  for select using (auth.uid() = id);
create policy "profiles_own_insert" on public.profiles
  for insert with check (auth.uid() = id);
create policy "profiles_own_update" on public.profiles
  for update using (auth.uid() = id);

-- Liderlik tablosu/profil kartı için yalnızca takma ad + avatar (E-POSTA YOK).
-- Görünüm sahibi ile çalıştığı için temel tablonun RLS'ini aşar; açılan sütunlar
-- burada tek tek yazılıdır — yeni sütun eklersen buraya EKLEME.
create or replace view public.public_profiles as
  select id, display_name, avatar_url from public.profiles;
grant select on public.public_profiles to anon, authenticated;

-- yeni kullanıcı kaydolunca profili otomatik oluştur
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, display_name, avatar_url, email)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'name', split_part(coalesce(new.email, 'oyuncu'), '@', 1)),
    new.raw_user_meta_data->>'avatar_url',
    new.email
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- 👥 toplam üye sayısı: sitede footer'da gösterilir (anon çağırabilir)
create or replace function public.user_count()
returns bigint
language sql stable
security definer set search_path = public
as $$ select count(*) from public.profiles $$;

grant execute on function public.user_count() to anon, authenticated;

-- 🏆 Skorlar: cihazlar arası liderlik tablosu (uygulama entegrasyonu sonraki adım)
create table if not exists public.scores (
  id bigint generated always as identity primary key,
  user_id uuid not null references public.profiles(id) on delete cascade,
  mode text not null,          -- 'notes' | 'ninja' | 'tetris' | ...
  score numeric not null,
  meta jsonb,
  created_at timestamptz not null default now()
);

alter table public.scores enable row level security;

create policy "scores_public_read" on public.scores
  for select using (true);
create policy "scores_own_insert" on public.scores
  for insert with check (auth.uid() = user_id);

create index if not exists scores_mode_score on public.scores (mode, score desc);
