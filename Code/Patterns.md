#Заместитель
Django ORM – часть фреймворка Django, которая позволяет программисту работать с экземплярами классов как с объектами базы данных, скрывая тем самым процесс обращения и работы с базой.

#Декоратор
Функция реализовывающая паттерн декоратор.
`@login_required
def profile_view(request, slug=None):
    if request.method == 'GET':
        if slug:
            user = UserManager.safe_get(slug__iexact=slug.lower())
            projects = user.get_all_projects()
            return render(request, 'profile/profile_page.html',
                          context={'user': user, 'projects': projects, 'request_user': request.user})
        else:
            projects = request.user.get_all_projects()
            return render(request, 'profile/profile_page.html',
                          context={'user': request.user, 'projects': projects, 'request_user': request.user})`
При вызове данной функции перед её исполнением вызывается функция оберкта login_required, проверяющая авторизацию пользователя.
`def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator`
 Если пользователь не авторизован выполняется функция запрашивающая авторизацию, иначе выполняется исходная функция.
