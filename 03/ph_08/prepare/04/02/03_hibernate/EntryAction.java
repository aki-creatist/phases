package action;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.HashMap;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.struts.action.ActionForm;
import org.apache.struts.action.ActionForward;
import org.apache.struts.action.ActionMapping;
import org.apache.struts.action.DynaActionForm;
import org.apache.struts.actions.LookupDispatchAction;
import org.hibernate.HibernateException;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import entity.Dept;
import entity.Emp;

public class EntryAction extends LookupDispatchAction {

    @Override
    protected Map<String, String> getKeyMethodMap() {
        Map<String, String> map = new HashMap<String, String>();
        map.put("label.button.entry.input", "input");
        map.put("label.button.entry.execute", "entry");
        return map;
    }

    public ActionForward input(ActionMapping mapping, ActionForm form,
            HttpServletRequest request, HttpServletResponse response)
            throws Exception {

        return mapping.findForward("input");
    }

    public ActionForward entry(ActionMapping mapping, ActionForm form,
            HttpServletRequest request, HttpServletResponse response)
            throws Exception {

        // 設定ファイルの読み込み
        Configuration config = new Configuration();
        config = config.configure();

        // セッションファクトリーの作成
        SessionFactory sessionFactory = config.buildSessionFactory();

        // セッションオブジェクトの作成
        Session session = sessionFactory.openSession();

        // トランザクションの開始
        Transaction trans = session.beginTransaction();

        try {
            // リクエストパラメータの値をエンティティにセット
            DynaActionForm dForm = (DynaActionForm) form;
            Emp emp = new Emp();
            Dept dept = new Dept();
            emp.setEmpId(Integer.parseInt((String) dForm.get("empId")));
            emp.setEmpPass((String) dForm.get("empPass"));
            emp.setEmpName((String) dForm.get("empName"));
            emp.setGender(Integer.parseInt((String) dForm.get("gender")));
            emp.setAddress((String) dForm.get("address"));
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
            emp.setBirthday(new Timestamp(sdf.parse(
                    (String) dForm.get("birthday")).getTime()));
            dept.setDeptId(Integer.parseInt((String) dForm.get("deptId")));
            emp.setDept(dept);

            // 登録
            session.save(emp);

            // コミット
            trans.commit();

        } catch (HibernateException e) {
            // ロールバック
            e.printStackTrace();
            trans.rollback();
        }

        // セッションオブジェクトのクローズ
        session.close();

        response.sendRedirect(request.getContextPath() + "/search.do");
        return null;
    }

}