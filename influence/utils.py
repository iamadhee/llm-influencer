import logging
import logging.handlers

def format_quotes(q_list):
    fquotes = ""
    for i,l in enumerate(q_list, 1):
        fquotes+=f"{i}) {l}\n"
    return fquotes

def setup_email_alerter(alert_email, app_pwd):
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.ERROR)
    logger = logging.getLogger(__name__)
    smtp_handler = logging.handlers.SMTPHandler(mailhost=('smtp.gmail.com', 587),
                                                fromaddr=alert_email,
                                                toaddrs=[alert_email],
                                                subject='LLM Influencer Job Failure',
                                                credentials=(
                                                    alert_email,
                                                    app_pwd),
                                                secure=())
    logger.addHandler(smtp_handler)
    return logger

def setup_custom_logger():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger
