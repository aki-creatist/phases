package entity;

import java.io.Serializable;
import java.util.Set;
import org.apache.commons.lang.builder.ToStringBuilder;


/** @author Hibernate CodeGenerator */
public class Dept implements Serializable {

    /** identifier field */
    private Integer deptId;

    /** persistent field */
    private String deptName;

    /** persistent field */
    private Set emps;

    /** full constructor */
    public Dept(Integer deptId, String deptName, Set emps) {
        this.deptId = deptId;
        this.deptName = deptName;
        this.emps = emps;
    }

    /** default constructor */
    public Dept() {
    }

    public Integer getDeptId() {
        return this.deptId;
    }

    public void setDeptId(Integer deptId) {
        this.deptId = deptId;
    }

    public String getDeptName() {
        return this.deptName;
    }

    public void setDeptName(String deptName) {
        this.deptName = deptName;
    }

    public Set getEmps() {
        return this.emps;
    }

    public void setEmps(Set emps) {
        this.emps = emps;
    }

    public String toString() {
        return new ToStringBuilder(this)
            .append("deptId", getDeptId())
            .toString();
    }

}