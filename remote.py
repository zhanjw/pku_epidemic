import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


class EmailReporter:

    def __init__(self, sender: str, password: str, receiver: str, server_addr: str, server_port: int = 25,
                 ssl: bool = False):
        self.sender = sender
        self.password = password
        if receiver is None:
            self.receiver = sender
        else:
            self.receiver = receiver
        self.server_addr = server_addr
        self.server_port = server_port
        self.enable_ssl = ssl
        self.server = smtplib.SMTP(self.server_addr, self.server_port)
        self.server.set_debuglevel(2)

    def login(self):
        if self.enable_ssl:
            self.server.starttls()
        self.server.login(self.sender, self.password)

    def send(self, message, subject):
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = self._format_addr('Notifier <%s>' % self.sender)
        msg['To'] = self._format_addr('Admin <%s>' % self.receiver)
        msg['Subject'] = Header(subject, 'utf-8').encode()
        self.server.sendmail(from_addr=self.sender, to_addrs=[self.receiver], msg=msg.as_string())

    @staticmethod
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def exit(self):
        self.server.quit()

