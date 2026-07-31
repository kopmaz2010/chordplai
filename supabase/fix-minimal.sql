-- ASGARİ DÜZELTME — yalnızca sızıntıyı kapatır, HİÇBİR VERİ SİLMEZ.
-- Sütun düşürme / e-posta temizleme YOK. Geri alınabilir (politika değişimi).
-- Panel: https://supabase.com/dashboard/project/cnpfhcjxxtboylvvqbfz/sql/new

begin;

-- Herkese açık okumayı kaldır, kendi satırına kilitle
drop policy if exists "profiles_public_read" on public.profiles;
drop policy if exists "profiles_own_read"    on public.profiles;
create policy "profiles_own_read" on public.profiles
  for select using (auth.uid() = id);

-- Liderlik tablosu/profil kartı için e-postasız görünüm
create or replace view public.public_profiles as
  select id, display_name, avatar_url from public.profiles;
grant select on public.public_profiles to anon, authenticated;

commit;

-- Geri almak istersen:
--   drop policy "profiles_own_read" on public.profiles;
--   create policy "profiles_public_read" on public.profiles for select using (true);
