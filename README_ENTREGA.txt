Projeto pronto para entrega.

Login unificado (usuário + admin) usando o mesmo template:
- Tela: templates/registration/login.html
- Rota usuário: /accounts/login/
- Admin: /admin (redireciona para /admin/login/ com a mesma tela)

Como rodar:
1) python -m venv .venv && ./.venv/Scripts/activate (Windows)
2) pip install Django==5.2.7 Pillow
3) python manage.py migrate
4) python manage.py createsuperuser
5) python manage.py runserver
