-- ACİL DÜZELTME — 31 Temmuz 2026
-- Sorun: profiles tablosunda "for select using (true)" politikası vardı.
-- anon anahtarı sitede herkese açık olduğu için, herkes tüm üyelerin
-- e-postasını, adını ve avatarını listeleyebiliyordu (553 kayıt).
--
-- Supabase panelinde çalıştır:
--   https://supabase.com/dashboard/project/cnpfhcjxxtboylvvqbfz/sql/new
-- Tamamını yapıştır → Run.

begin;

-- 1) Herkese açık okumayı kaldır, kendi satırına kilitle
drop policy if exists "profiles_public_read" on public.profiles;
drop policy if exists "profiles_own_read"    on public.profiles;
create policy "profiles_own_read" on public.profiles
  for select using (auth.uid() = id);

-- 2) Sıralama/profil kartı için yalnızca takma ad + avatar (E-POSTA YOK)
create or replace view public.public_profiles as
  select id, display_name, avatar_url from public.profiles;
grant select on public.public_profiles to anon, authenticated;

commit;

-- ---------------------------------------------------------------
-- DOĞRULAMA (çalıştırdıktan sonra terminalde):
--
--   cd ~/akor-antrenoru
--   ANON=$(grep -o 'anon: *"[^"]*"' index.html | head -1 | sed 's/.*"\(.*\)"/\1/')
--   BASE=https://cnpfhcjxxtboylvvqbfz.supabase.co
--
--   # Bu BOŞ dizi [] dönmeli (artık e-posta sızmıyor):
--   curl -s "$BASE/rest/v1/profiles?select=email&limit=5" -H "apikey: $ANON"
--
--   # Bu takma adları dönmeli (liderlik tablosu çalışmaya devam ediyor):
--   curl -s "$BASE/rest/v1/public_profiles?select=display_name&limit=5" -H "apikey: $ANON"
--
--   # Üye sayacı bozulmamalı (security definer olduğu için etkilenmez):
--   curl -s -X POST "$BASE/rest/v1/rpc/user_count" -H "apikey: $ANON" \
--        -H "Content-Type: application/json" -d '{}'
-- ---------------------------------------------------------------
