The Vanilla JS implementation of the application.

In order to run it, first you need to build the JavaScript and CSS:

```bash
# One-time set-up step
npm install

npm run build
gulp styles
gulp scripts
```

Then, start the backend server:

```bash
cd ../backend
virtualenv .venv
./manage.py runserver
```

Visit http://localhost:8000/vanilla in your browser to see the application.