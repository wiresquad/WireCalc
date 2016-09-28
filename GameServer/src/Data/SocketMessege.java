/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Data;

import java.io.*;
import java.util.logging.Level;
import java.util.logging.Logger;
/**
 *
 * @author xguest
 */
public class SocketMessege implements Serializable {
    public String messege;
    
    public SocketMessege(String mes){
        messege = mes;
    }
    
    public static byte[] getMessegeBytes(SocketMessege msg){    
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos;
        
        try {
            oos = new ObjectOutputStream(baos);
            oos.writeObject(msg);
        } catch (IOException ex) {
            Logger.getLogger(SocketMessege.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        byte[] data = baos.toByteArray();
        
        
        return data;
    }
    
    public static SocketMessege getMessegeSocket(byte[] msg){
        ByteArrayInputStream bais = new ByteArrayInputStream(msg);
        SocketMessege answer = null;
        try {
            ObjectInputStream ois = new ObjectInputStream(bais);
            Object readObject = ois.readObject();
            
            if (readObject instanceof SocketMessege) {
                answer = (SocketMessege) readObject;
            } else {
                System.out.println("The received object is not of type SocketMessege!");
            }
        } catch (Exception e) {
            System.out.println("No object could be read from the received UDP datagram.");
        }
        
        return answer;
    }
}
