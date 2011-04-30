from django.core.management.base import BaseCommand
import pexpect
class Command(BaseCommand):
    def handle(self, *args, **options):
        username = 'semarjt'
        server_name = 'btcserver'
        try:
            domain = args[1]
        except IndexError:
            domain = 'bitcoinpalace.com'
        command = 'cd /var/www/%s && sudo -u www-data git reset --hard && sudo -u www-data git pull && sudo ./manage.py migrate && sudo /etc/init.d/apache2 restart' % server_name
        p = pexpect.spawn('ssh -t %s@%s %s' % (username, domain, command))
        p.interact()
