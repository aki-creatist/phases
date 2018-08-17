package sample01;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.struts.action.Action;
import org.apache.struts.action.ActionForm;
import org.apache.struts.action.ActionForward;
import org.apache.struts.action.ActionMapping;

public class LoginAction extends Action{
    public ActionForward execute(ActionMapping mapping,
                                ActionForm form,
                                HttpServletRequest request,
                                HttpServletResponse response)
            throws Exception{

        // ActionformをLoginFormにキャスト
        LoginForm loginForm = (LoginForm)form;

        // フォームに入力されたIDを取得する
        String id = loginForm.getId();

        // フォームに入力されたパスワードを取得する
        String password = loginForm.getPassword();
        String message = " ID:" + id + " パスワード:" + password;

        // messageをrequestスコープに登録する
        request.setAttribute("message",message);

        // ActionForwardを返却
        return mapping.findForward("success");
    }
}