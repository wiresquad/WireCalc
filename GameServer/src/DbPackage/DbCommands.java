package DbPackage;
import com.mysql.jdbc.*;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Connection;


public class DbCommands {
    
    Connection conn = null;
    
    public void Connect(){
        try
        {
        
        conn=DriverManager.getConnection("jdbc:mysql://localhost/test?" +
                                   "user=minty&password=greatsqldb");
        }
        
    catch (SQLException ex)
    {
    // handle any errors
    System.out.println("SQLException: " + ex.getMessage());
    System.out.println("SQLState: " + ex.getSQLState());
    System.out.println("VendorError: " + ex.getErrorCode());
    }   
    }
      
    public void firstSelect(){
        Connect();
        
    }
}
