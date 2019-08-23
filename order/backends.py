from django.contrib.auth import get_user_model
import inspect
from shibboleth.backends import ShibbolethRemoteUserBackend


class LsdfUserBackend(ShibbolethRemoteUserBackend):

    def authenticate(self, request, remote_user, shib_meta):
        """
        The username passed as ``remote_user`` is considered trusted.  This
        method simply returns the ``User`` object with the given username,
        creating a new ``User`` object if ``create_unknown_user`` is ``True``.

        Returns None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
        if not remote_user:
            return
        User = get_user_model()
        username = self.clean_username(remote_user)
        field_names = [x.name for x in User._meta.get_fields()]
        shib_user_params = dict([(k, shib_meta[k]) for k in field_names if k in shib_meta])
        email = self.clean_username(shib_user_params.email)
        # Note that this could be accomplished in one try-except clause, but
        # instead we use get_or_create when creating unknown users since it has
        # built-in safeguards for multiple threads.
        if self.create_unknown_user:

            created = False
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=username)
                    user.username = username
                except User.DoesNotExist:
                    user = User(username=username, defaults=shib_user_params)
                    created = True
            if created:
                """
                @note: setting password for user needs on initial creation of user instead of after auth.login() of middleware.
                because get_session_auth_hash() returns the salted_hmac value of salt and password.
                If it remains after the auth.login() it will return a different auth_hash
                than what's stored in session "request.session[HASH_SESSION_KEY]".
                Also we don't need to update the user's password everytime he logs in.
                """
                user.set_unusable_password()
                user.save()
                args = (request, user)
                try:
                    inspect.signature(self.configure_user).bind(request, user)
                except AttributeError:
                    # getcallargs required for Python 2.7 support, deprecated after 3.5
                    try:
                        inspect.getcallargs(self.configure_user, request, user)
                    except TypeError:
                        args = (user,)
                except TypeError:
                    args = (user,)
                user = self.configure_user(*args)
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return
        # After receiving a valid user, we update the the user attributes according to the shibboleth
        # parameters. Otherwise the parameters (like mail address, sure_name or last_name) will always
        # be the initial values from the first login. Only save user object if there are any changes.
        if not min([getattr(user, k) == v for k, v in shib_user_params.items()]):
            user.__dict__.update(**shib_user_params)
            user.save()
        return user if self.user_can_authenticate(user) else None

