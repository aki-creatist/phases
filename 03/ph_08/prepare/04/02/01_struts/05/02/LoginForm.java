package sample01;

import org.apache.struts.action.ActionForm;

public class LoginForm extends ActionFrom{

    // リクエストパラメータ名と同じフィールド
    private String id = null;
    private String password = null;

    // getter/setterメソッド
    public String getId(){
        return id;
    }

    public String getPassword(){
        return pqssword;
    }

    public void setId(String id){
        this.id = id;
    }

    public void setPassword(String password){
        this.password = password;
    }
}