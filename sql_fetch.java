import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class Main {
   public static void main(String[] argv) throws Exception {
        Connection conn = getGoogleCloudDBConnection();
        Statement stmt = conn.createStatement();  
        ResultSet rs = stmt.executeQuery("select * from barcodes where user = 'gdai'");  
        while(rs.next()){
            String barcode = rs.getString(2);
        }
        con.close();
    }

    public static Connection getGoogleCloudDBConnection() throws Exception {

        Class.forName("com.mysql.jdbc.Driver").newInstance();
        Connection conn = null;

        try {
            String url = "jdbc:mysql://34.155.207.12:3306/testdb";
            String user = "root";
            String pass = "pi1234";
            conn = DriverManager.getConnection(url, user, pass);

        } catch (SQLException ex) {
            // handle any errors
            System.out.println("SQLException: " + ex.getMessage());
            System.out.println("SQLState: " + ex.getSQLState());
            System.out.println("VendorError: " + ex.getErrorCode());
        }

        return conn;
    }
}