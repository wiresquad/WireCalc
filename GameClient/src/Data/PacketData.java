package Data;

import org.json.simple.*;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

/**
 *
 * @author xguest
 */
public class PacketData {
    int status=0;
    String msg="";
    int x=-1,y=-1;
    JSONObject obj=null;
    
    public PacketData(byte[] data, int length) {
        try {
            //obj=new JSONObject(data.toString());
            JSONParser parser = new JSONParser();
            String dataString = new String(data,0,length);
            obj = (JSONObject)parser.parse(dataString);
        } catch (ParseException ex) {
            System.out.println(ex);
        }
        
    }

    public PacketData() {
        
    }
    
    public void setStatus(int status){
        this.status=status;
    }
    
    public void setMsg(String msg){
        this.msg=msg;
    }
    
    public void setCord(int x,int y){
        this.x=x;
        this.y=y;
    }
    
    public byte[] getData(){
        obj=new JSONObject();
        obj.put("status", new Integer(status));
        obj.put("msg", new String(msg));
        obj.put("x", new Integer(x));
        obj.put("y", new Integer(y));
        return obj.toJSONString().toString().getBytes();
    }
    
    public int getStatus(){
        return Integer.parseInt(obj.get("status").toString());
    }
    
    public String getMsg(){
        return obj.get("msg").toString();
    }
    
    public int getX(){
        return Integer.parseInt(obj.get("x").toString());
    }
    
    public int getY(){
        return Integer.parseInt(obj.get("y").toString());
    }
    
    
}
