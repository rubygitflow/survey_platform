# survey_platform
This is

**The Survey Platform application, which contains the following features:**
- Creating and editing surveys and questions through the admin panel;
- User navigation through surveys to collect answers to questions;
- Saving user responses in conjunction with relevant questions;

**The application includes:**
- Admin panel;
- User Interface;
- A logical tree that allows you to determine which questions to show or hide, depending on the user's previous answers;
- The output of the survey results, including statistics on the answers to each question, after the survey is completed.

Based on an idea from https://nomia2.notion.site/Python-developer-7adf62ee6a9f4aaab28db4ac661e2139

### Install the database with the source data
1. Add environment variables to the `survey_platform/.env` file (look at `survey_platform/.env.example`).
2. `python manage.py migrate --fake-initial`
3. `./manage.py loaddata seeds.json`
