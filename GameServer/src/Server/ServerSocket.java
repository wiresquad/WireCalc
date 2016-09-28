package Server;

import Users.UserManager;
import java.io.*;
import java.net.*;
/**
 *
 * @author xguest
 */
public class ServerSocket {
    final static int PORT = 8080;

    public static void main(String[] args){
        DatagramSocket sock = null;
        Users.UserManager users = new UserManager(); 
        
        try{
            sock = new DatagramSocket(PORT);
             
            //buffer to receive incoming data
            byte[] buffer = new byte[65536];
            DatagramPacket incoming = new DatagramPacket(buffer, buffer.length);
            
            System.out.println("Waiting for clients...");
             
            //communication loop
            while(true){
                sock.receive(incoming);
                (new Thread(new PacketResponser(users, sock, incoming))).start();
            }
        }catch(IOException e){
            System.err.println(e);
        }
    }
}
