graph_url = 'https://graph.facebook.com/v17.0/'
import requests

def post_image(caption='', image_url='',instagram_account_id='',access_token=''):
    url = graph_url + instagram_account_id + '/media'
    param = dict()
    param['access_token'] = access_token
    param['caption'] = caption
    param['image_url'] = image_url
    response = requests.post(url, params=param, verify=False)
    response = response.json()
    return response