package entity;

import java.io.Serializable;
import java.util.Date;
import org.apache.commons.lang.builder.ToStringBuilder;


/** @author Hibernate CodeGenerator */
public class Emp implements Serializable {

    /** identifier field */
    private Integer empId;

    /** persistent field */
    private String empPass;

    /** persistent field */
    private String empName;

    /** persistent field */
    private int gender;

    /** persistent field */
    private String address;

    /** persistent field */
    private Date birthday;

    /** persistent field */
    private entity.Dept dept;

    /** full constructor */
    public Emp(Integer empId, String empPass, String empName, int gender, String address, Date birthday, entity.Dept dept) {
        this.empId = empId;
        this.empPass = empPass;
        this.empName = empName;
        this.gender = gender;
        this.address = address;
        this.birthday = birthday;
        this.dept = dept;
    }

    /** default constructor */
    public Emp() {
    }

    public Integer getEmpId() {
        return this.empId;
    }

    public void setEmpId(Integer empId) {
        this.empId = empId;
    }

    public String getEmpPass() {
        return this.empPass;
    }

    public void setEmpPass(String empPass) {
        this.empPass = empPass;
    }

    public String getEmpName() {
        return this.empName;
    }

    public void setEmpName(String empName) {
        this.empName = empName;
    }

    public int getGender() {
        return this.gender;
    }

    public void setGender(int gender) {
        this.gender = gender;
    }

    public String getAddress() {
        return this.address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public Date getBirthday() {
        return this.birthday;
    }

    public void setBirthday(Date birthday) {
        this.birthday = birthday;
    }

    public entity.Dept getDept() {
        return this.dept;
    }

    public void setDept(entity.Dept dept) {
        this.dept = dept;
    }

    public String toString() {
        return new ToStringBuilder(this)
            .append("empId", getEmpId())
            .toString();
    }

}