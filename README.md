# Лабораторная работа 9

Интеграция автоматизированных тестов в CI/CD (GitHub Actions).
Дисциплина: Тестирование программного обеспечения.

Взята проверка успешного входа из лабораторной работы 3: Selenium открывает
https://the-internet.herokuapp.com/login, вводит опубликованные на учебном сайте
данные `tomsmith` / `SuperSecretPassword!` и проверяет адрес `/secure`, кнопку
Logout и сообщение об успешном входе. Это общедоступная учебная учётная запись.

## Локальный запуск на macOS или Linux

Нужны Python 3.12, Google Chrome и доступ к интернету. В терминале из папки проекта:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest --headless -v --junitxml=reports/junit.xml
```

Windows PowerShell: создайте окружение командой `py -3.12 -m venv .venv`,
далее используйте `.venv\Scripts\python.exe -m pip install -r requirements.txt`
и `.venv\Scripts\python.exe -m pytest --headless -v --junitxml=reports/junit.xml`.

Для запуска с видимым Chrome уберите `--headless`.
ChromeDriver подбирается автоматически через webdriver-manager. Результат:
`1 passed`, код завершения 0; скриншот `artifacts/successful_login.png`,
JUnit XML `reports/junit.xml`. Сбой сайта или доступа к нему приводит к падению
теста; ошибки не скрываются повторными попытками или `continue-on-error`.

## Публикация и проверка CI

Публикуйте содержимое этой папки как корень отдельного репозитория.
Файл должен находиться по пути `.github/workflows/run-tests.yml` от его корня.
Отчёт Word с личными данными загружать в публичный репозиторий не требуется.

После входа через `gh auth login --hostname github.com --web`:

```sh
git init -b main
git add .
git commit -m "Add Selenium tests and GitHub Actions workflow"
gh repo create tpo-lab9-ci --public --source=. --remote=origin --push
gh run list --limit 5
```

Если Git попросит имя и почту автора, задайте свои значения через
`git config user.name` и `git config user.email` и повторите commit.
Не создавайте репозиторий повторно, если он уже существует.

Откройте Actions → Automated tests → последний запуск. Дождитесь статуса
Success и зелёной галочки у задания Pytest on Ubuntu. В шаге Run pytest
должна быть строка `1 passed`. Сохраните ссылку на запуск и его скриншот
для подтверждения пункта 4 задания.

Workflow запускается при каждом push, pull request и вручную из Actions
(Run workflow). GitHub выделяет готовую виртуальную машину Ubuntu 24.04;
setup-python выбирает Python 3.12; pip устанавливает зависимости; pytest
запускает тест в Chrome без окна. JUnit XML создаётся на runner, а результат
и текст pytest доступны в журнале шага Run pytest.

Для повторной демонстрации после первого успешного запуска:

```sh
git commit --allow-empty -m "Trigger CI demonstration"
git push
gh run list --limit 5
```

## Источники

- [GitHub Actions для Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
- [actions/checkout](https://github.com/actions/checkout)
- [actions/setup-python](https://github.com/actions/setup-python)

В этом задании реализована стадия непрерывной интеграции (CI).
Развёртывание приложения (CD) в задание не входит.
