# DeadDevelopers — Account Provisioning Runbook

Step-by-step setup for every external account/credential the deployed site
needs. Do these in order. Total time: ~45–75 minutes if you're new to all
services, ~20–30 if you've used them before.

At the end you'll have every value needed to fill in `.env.production`
and Vercel's environment-variables panel.

---

## 0. What you need before starting

- A credit card on file with each provider (most have a free tier; Vercel
  Postgres and GCS will charge for usage past the free quota).
- A domain name if you want a custom URL — **optional**, Vercel gives you
  a `*.vercel.app` URL for free.
- Around 30–60 minutes of uninterrupted time. You'll be copying short
  strings between dashboards.

Keep a scratch file open. Every "**Save:**" line below is a value you'll
paste into Vercel's env vars later.

---

## 1. Vercel (5–10 min)

The host. Owns the deployment + the Postgres database + the KV cache.

### 1.1 Create the project
1. Go to <https://vercel.com/signup>. Sign up with the GitHub account that
   owns `paradiselabs-ai/DeadDevelopers`.
2. After signup, click **Add New… → Project**.
3. Find **paradiselabs-ai/DeadDevelopers** in the import list. Click
   **Import**.
4. On the configure screen:
   - Framework Preset: **Other** (Vercel doesn't auto-detect FastHTML).
   - Build Command: leave blank.
   - Output Directory: leave blank.
   - Root Directory: leave at repo root.
5. Click **Deploy**. The first deploy WILL fail — that's expected, env
   vars aren't set yet. Don't panic.

### 1.2 Get project IDs
1. In the project, go to **Settings → General**.
2. **Save:** `Project ID` → this is `VERCEL_PROJECT_ID`.
3. In the URL bar, the segment between `vercel.com/` and the project
   slug is your team/personal slug. Click your avatar (top right) →
   **Account Settings → General**.
4. **Save:** `Your ID` → this is `VERCEL_ORG_ID`.

### 1.3 Add Postgres
1. In the project, go to **Storage → Create Database → Postgres**.
2. Pick a name (e.g. `deaddevs-db`) and a region close to your users.
3. Click **Create**.
4. Once created, click the database → **`.env.local`** tab.
5. **Save:** `POSTGRES_URL` (the full `postgres://...` string).
   - You can also use `POSTGRES_PRISMA_URL` if Vercel offers it; either
     works for Django.

### 1.4 Add KV (Redis-compatible cache)
1. **Storage → Create Database → KV**.
2. Name it (e.g. `deaddevs-cache`), pick the same region as Postgres.
3. **Create.**
4. Click into it → **`.env.local`** tab.
5. **Save:** `KV_URL` (the `redis://...` string).

---

## 2. OpenRouter (3 min)

The AI assistant backend. One key, every model.

1. Go to <https://openrouter.ai>. Sign in with GitHub or Google.
2. Add **$5–$10 of credits** at <https://openrouter.ai/credits>. With
   `claude-haiku-4-5` at ~$0.80 per 1M tokens, $5 covers thousands of
   user messages.
3. Go to <https://openrouter.ai/keys>.
4. Click **Create Key**. Name it `deaddevelopers-prod`. Leave the spend
   limit at the default unless you want a hard cap.
5. **Save:** the key (starts with `sk-or-v1-...`) → this is
   `OPENROUTER_API_KEY`.
6. Browse <https://openrouter.ai/models> to confirm
   `anthropic/claude-haiku-4-5` is the model you want as default. If you
   prefer cheaper, `meta-llama/llama-3.3-70b-instruct` is solid;
   `google/gemini-flash-2.0` is even cheaper.
7. **Save:** chosen model id → `OPENROUTER_DEFAULT_MODEL`. (Optional —
   defaults to `anthropic/claude-haiku-4-5` if unset.)

---

## 3. GitHub OAuth App (5 min)

Lets users sign in with GitHub.

1. Go to <https://github.com/settings/developers> → **OAuth Apps → New
   OAuth App**.
2. Fill in:
   - Application name: `DeadDevelopers`
   - Homepage URL: `https://your-vercel-url.vercel.app` (or your custom
     domain if you set one — you can edit this later).
   - Authorization callback URL:
     `https://your-vercel-url.vercel.app/accounts/github/login/callback/`
3. Click **Register application**.
4. **Save:** `Client ID` → `GITHUB_CLIENT_ID`.
5. Click **Generate a new client secret**.
6. **Save:** the secret (shown once) → `GITHUB_CLIENT_SECRET`.

> Once you know your final Vercel URL or custom domain, come back and
> update Homepage URL + Callback URL accordingly. The callback path
> `/accounts/github/login/callback/` is hardcoded by django-allauth.

---

## 4. Google Cloud Storage (10–15 min)

Stores user-uploaded avatars and portfolio images. Skip this section if
you're OK with avatars living in `/media/` on the deploy host (works on
Vercel for the duration of a deployment but won't persist across
deploys — fine for early users, not long-term).

### 4.1 Create the project + bucket
1. Go to <https://console.cloud.google.com>. If first time, agree to
   terms and start the free trial ($300 credit, no auto-charge).
2. Top bar → **Select a project → New Project**.
3. Name: `deaddevelopers`. Click **Create**.
4. Wait for creation, then select the project from the top bar.
5. **Save:** the Project ID (under your project name) → `GCS_PROJECT_ID`.
6. In the search bar, type `Cloud Storage` → click the result.
7. **Create bucket**:
   - Name: `deaddevelopers-media` (must be globally unique — add a
     suffix like `-prod` or your username if taken).
   - Region: pick the same one as your Vercel deployment.
   - Storage class: **Standard**.
   - Access control: **Uniform**.
   - Public access prevention: **Off** (avatars are public-by-design;
     see `django_config/storage.py` for the privacy note).
   - Click **Create**.
8. **Save:** the bucket name → `GCS_BUCKET_NAME`.

### 4.2 Service account + key
1. In the search bar: `IAM & Admin → Service Accounts`. Click result.
2. **Create Service Account**:
   - Name: `deaddevs-storage`.
   - Click **Create and continue**.
   - Role: **Storage Object Admin** (full bucket read/write).
   - Click **Continue → Done**.
3. Click the new service account → **Keys → Add Key → Create new key**
   → **JSON** → **Create**.
4. A `.json` file downloads. Open it.
5. **For Vercel**: copy the entire JSON contents. You'll paste it into
   Vercel as a single env var named `GCS_CREDENTIALS_JSON` (we read it
   in `django_config/storage.py` and write it to a tmp file at runtime
   — this is the standard Vercel-compatible pattern).
6. **Save:** the JSON contents → `GCS_CREDENTIALS_JSON` (multi-line OK,
   Vercel handles it).

> If you skip GCS, leave `GCS_CREDENTIALS_JSON` blank — `MediaStorage`
> auto-falls-back to local filesystem storage.

---

## 5. Email / SMTP (5 min — pick one)

Used for password resets and email confirmation. **Auto-verification is
ON in dev mode**, so you can defer this until after first deploy if you
want.

### Option A: Resend (recommended — generous free tier, easy setup)
1. <https://resend.com/signup>.
2. Verify your sending domain (or use the free `onboarding@resend.dev`
   for testing only).
3. <https://resend.com/api-keys> → **Create API Key**.
4. **Save:**
   - `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
   - `EMAIL_HOST=smtp.resend.com`
   - `EMAIL_PORT=587`
   - `EMAIL_USE_TLS=True`
   - `EMAIL_HOST_USER=resend`
   - `EMAIL_HOST_PASSWORD=` (your API key)
   - `DEFAULT_FROM_EMAIL=noreply@yourdomain.com`

### Option B: Gmail (works but flaky for production, fine for testing)
1. Enable 2FA on your Google account.
2. <https://myaccount.google.com/apppasswords> → generate an app
   password for "Mail."
3. **Save:**
   - `EMAIL_HOST=smtp.gmail.com`
   - `EMAIL_PORT=587`
   - `EMAIL_USE_TLS=True`
   - `EMAIL_HOST_USER=your-gmail@gmail.com`
   - `EMAIL_HOST_PASSWORD=` (the 16-char app password, no spaces)
   - `DEFAULT_FROM_EMAIL=your-gmail@gmail.com`

---

## 6. Generate Django + FastHTML secret keys (1 min)

Two cryptographic secrets — never reuse, never commit.

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Run twice. **Save:**
- First output → `SECRET_KEY` (Django).
- Second output → `FASTHTML_SECRET_KEY`.

---

## 7. (Optional, defer) Stripe + Hashnode

Both are present in `.env.example` but not currently wired into the
shipping app. **Skip unless/until you build the corresponding feature.**

- Stripe: needed only if you add paid plans. <https://dashboard.stripe.com>.
- Hashnode: needed only if you wire the blog integration.
  <https://hashnode.com/settings/developer>.

---

## 8. Wire everything into Vercel (10 min)

1. Vercel project → **Settings → Environment Variables**.
2. For each value you saved above, click **Add**:
   - Key: the variable name (e.g. `OPENROUTER_API_KEY`).
   - Value: the saved value.
   - Environment: check **Production** (and **Preview** if you want
     branch deploys to also work).
3. Required minimum to ship:
   - `SECRET_KEY`
   - `FASTHTML_SECRET_KEY`
   - `DJANGO_DEBUG=False`
   - `ALLOWED_HOSTS=.vercel.app,yourdomain.com`
   - `POSTGRES_URL`
   - `KV_URL`
   - `OPENROUTER_API_KEY`
   - `OPENROUTER_DEFAULT_MODEL=anthropic/claude-haiku-4-5`
   - `SITE_URL=https://your-vercel-url.vercel.app`
   - `GITHUB_CLIENT_ID`
   - `GITHUB_CLIENT_SECRET`
   - `EMAIL_*` (set of 6, see section 5)
   - `DEFAULT_FROM_EMAIL`
4. Optional (only if you did GCS in section 4):
   - `GCS_BUCKET_NAME`
   - `GCS_PROJECT_ID`
   - `GCS_CREDENTIALS_JSON` (the JSON blob, not a file path)
5. After saving all envs, click **Deployments → … → Redeploy** on the
   latest deployment to pick them up.

---

## 9. Post-deploy smoke test

Once Vercel reports the deploy as successful, hit these URLs in order:

1. `/` — landing page renders.
2. `/signup` — create a test account.
3. `/login` — log in with the same credentials.
4. `/dashboard` — should show project cards + AI ask widget.
5. `/dashboard/ask` (POST via the form) — type a question, confirm a
   real AI reply comes back. **If you see "AI assistant not configured"
   the OpenRouter key isn't reaching the function.**
6. `/profile/<your-username>` — your own profile loads.
7. `/profile/<your-username>/edit` — change bio, save, reload, change
   persists.
8. `/chat` — chat home with the global room visible.
9. `/chat/global` — join the global room, send a message.
10. `/api/profiles/me/` — JSON of your profile.

If any step fails, check Vercel logs (project → **Deployments → click
deploy → Runtime Logs**).

---

## 10. Domain (optional)

Project → **Settings → Domains → Add**. Follow Vercel's DNS
instructions. After it propagates:
- Update `ALLOWED_HOSTS` to include the bare domain.
- Update `SITE_URL` to the new URL.
- Update GitHub OAuth Homepage + Callback URLs (section 3) to the new
  domain.
- Redeploy.

---

## Cost ballpark (first 1k users)

- Vercel Hobby: free
- Vercel Postgres: ~$0–5/mo (free up to 256MB)
- Vercel KV: ~$0–1/mo (free tier covers light use)
- OpenRouter: depends entirely on usage. ~$0.80/1M tokens with Haiku
  4.5; 1k active users sending 5 messages/day each at ~500 tokens
  per round-trip ≈ $1/day, $30/mo. Set a hard credit cap on
  OpenRouter to prevent runaway.
- GCS: ~$0.02/GB-month + bandwidth. Avatars are tiny; expect <$1/mo.
- Resend: free up to 3k emails/month.
- GitHub OAuth: free.

**Total at small scale: ~$30–50/mo, almost all of it OpenRouter.**

---

## Done

Tell the agent "provisioned" once Vercel reports a successful deploy
and section 9's smoke test passes. The agent will run the formal
verification pass and confirm launch.
