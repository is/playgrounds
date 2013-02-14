package us.yuxin.demo.jsch;


import javax.security.auth.callback.CallbackHandler;
import javax.security.auth.login.LoginContext;
import javax.security.auth.login.LoginException;

import com.sun.security.auth.callback.TextCallbackHandler;

public class Krb5Init {
  public static void main(String args[]) throws LoginException
  {
    LoginContext lc = new LoginContext(Krb5Init.class.getName(), new TextCallbackHandler());
    lc.login();
  }
}
