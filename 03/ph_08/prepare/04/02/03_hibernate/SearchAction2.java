package action;

import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.struts.action.Action;
import org.apache.struts.action.ActionForm;
import org.apache.struts.action.ActionForward;
import org.apache.struts.action.ActionMapping;
import org.apache.struts.action.DynaActionForm;
import org.hibernate.Criteria;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;
import org.hibernate.criterion.Restrictions;

import entity.Emp;

public class SearchAction extends Action {

    public ActionForward execute(ActionMapping mapping, ActionForm form,
            HttpServletRequest request, HttpServletResponse response)
            throws Exception {

        // 設定ファイルの読み込み
        Configuration config = new Configuration();
        config = config.configure();

        // セッションファクトリーの作成
        SessionFactory sessionFactory = config.buildSessionFactory();

        // セッションオブジェクトの作成
        Session session = sessionFactory.openSession();

        Criteria criteria = session.createCriteria(Emp.class);

        // 検索値の取得
        DynaActionForm dForm = (DynaActionForm) form;
        String empName = (String) dForm.get("empName");

        // 検索条件の指定
        if (empName != null && !empName.isEmpty()) {
            criteria = criteria.add(Restrictions.ilike("empName", "%" + empName + "%"));
        }

        List<Emp> empList = criteria.list();

        // セッションオブジェクトのクローズ
        session.close();

        request.setAttribute("empList", empList);

        return mapping.findForward("success");
    }
}