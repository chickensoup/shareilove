
SOCIALOAUTH_SITES = {
    'renren': ('socialoauth.sites.renren.RenRen',
               {
                'redirect_uri': 'http://shareilove.org/account/oauth/renren',
                'client_id': '1797aa8579004e2cbf04b25136871a6a',
                'client_secret': 'c98f7849bf8648d298a3914fb3ad289a',
                'scope': ['publish_feed', 'status_update']
               }
    ),
        
    'weibo': ('socialoauth.sites.weibo.Weibo',
              {
                'redirect_uri': 'http://shareilove.org/account/oauth/weibo',
                'client_id': 'YOUR ID',
                'client_secret': 'YOUR SECRET',
              }
    ),
    
    'qq': ('socialoauth.sites.qq.QQ',
              {
                'redirect_uri': 'http://shareilove.org/account/oauth/qq',
                'client_id': '100455018',
                'client_secret': '3b805601e479c02c10750ab16ed7026c',
              }
    )    
}
