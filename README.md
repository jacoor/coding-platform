# coding-platform
For pymasters

MESSY - nEEDS UPDATE


### Testing

The project is using Pytest for automated testing. https://docs.pytest.org/

To run the tests first start project environment with:

```bash
poetry shell
```

Run tests in project directory with:

```bash

pytest -n auto -vv
```
This command runs tests in parallel, thus much faster.

Make sure all tests pass before creating PR. Automated tests are run on every PR and if tests fail, merge will not be possible.

#### Writing own tests

This is most welcome. Test should be located in `tests` directory of a module (remember to add `__init__.py` file!). 
Test filename should follow pattern `test_{name}.py` where name is either functionality or, eg. "models", so `test_models.py`.
Each test in the file must start with `test_` prefix, otherwise Pytest will not find it. 

Test driven development is most welcome, check https://www.youtube.com/watch?v=xn3wSM82fnA. It is understandable that TDD itself 
is cumbersome, so writing the tests after the code is also OK. Practice, practice, practice. Review other tests, experiment, and if questions, ask. 


#### Connecting gmail to the application

To enable registration on the site, you must provide your e-mail data. There are two ways.

In the env file you need to set these fields
   ```
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_HOST_USER = 'your_name_email@gmail.com'
   EMAIL_USE_TLS = True
   ```

1. First possibility.

   You enter your account password.

   ```
     EMAIL_HOST_PASSWORD = 'your_password'
   ```
2.  Second possibility.

      You can generate a token for your account instead of entering your password.
   

   ```
  * The first thing you need to do is go to https://myaccount.google.com/security
  * Activate two-step verification via this link https://myaccount.google.com/signinoptions/twosv
  * Then we return to the website https://myaccount.google.com in the input we enter app passwords or in Polish version "hasła do aplikacji" ( it depends on the language setting on your account )
  * after entering a given view, you must enter the password from your Gmail, then enter the name of this code.
  * Gmail returns you a code that you enter into the env file (EMAIL_HOST_PASSWORD).
   ```

## Setting Up Google Login in Django

This guide will help you set up Google OAuth login in a Django project using environment variables for client credentials.

### 1. Create Google OAuth Credentials

#### Step 1: Go to Google Cloud Console

- Navigate to [Google Cloud Console](https://console.cloud.google.com/).
- Make sure you're logged in with the Google account you want to use.

#### Step 2: Create a New Project (if needed)

- In the top navigation bar, click on the project dropdown.
- Select **New Project** if you don't have an existing one.
- Give your project a name and click **Create**.

#### Step 3: Enable the OAuth Consent Screen

1. In the left sidebar, go to **API & Services > OAuth consent screen**.
2. Select **External** if you want users outside your organization to log in (e.g., for testing purposes).
3. Fill in the required fields, such as **App Name**, **User Support Email**, and **Developer Contact Information**.
4. Click **Save and Continue**.

#### Step 4: Set Up OAuth Credentials

1. In the left sidebar, go to **API & Services > Credentials**.
2. Click **Create Credentials** and select **OAuth client ID**.
3. Choose **Web application** as the Application type.
4. Enter a name for the client, like `Django Google Login`.
5. In the **Authorized JavaScript origins** section, add:.

   - If running locally, the URI should look like this:
     ```
     http://127.0.0.1:8000
     ```
6. Under **Authorized redirect URIs**, add the redirect URI for your Django app.

   - If running locally, the URI should look like this:
     ```
     http://127.0.0.1:8000/users/google/complete/google-oauth2/
     ```
   
7. Click **Create**. Google will generate a **Client ID** and **Client Secret**.

8. Copy the **Client ID** and **Client Secret**. You will use these in your `.env` file.

#### Step 5: Save and wait for propagation

After saving, changes can take from 5 minutes to a few hours to take effect.

### 2. Configure Your `.env` File

1. Open the `.env` file in the root of your Django project (create it if it doesn’t exist).
2. Add the following environment variables from Step 4.8, replacing default values in `GOOGLE_OAUTH2_KEY` and `GOOGLE_OAUTH2_SECRET`.


### Ruff formatting and linting

This is how we use linter:
```bash
ruff check                  # Lint all files in the current directory.
ruff check --fix            # Lint all files in the current directory, and fix any fixable errors.
ruff check --watch          # Lint all files in the current directory, and re-lint on change.
ruff check path/to/code/    # Lint all files in `path/to/code` (and any subdirectories).
```


This is how to use formatter:
```bash
ruff format                   # Format all files in the current directory.
ruff format path/to/code/     # Format all files in `path/to/code` (and any subdirectories).
ruff format path/to/file.py   # Format a single file.
ruff format --check           # Checks if formatting is proper and reports violations. Does not change files.
```

More at:
https://docs.astral.sh/ruff/linter/
https://docs.astral.sh/ruff/formatter/
