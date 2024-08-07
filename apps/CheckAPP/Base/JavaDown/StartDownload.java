package com;
import org.apache.hc.client5.http.fluent.Request;
public class StartDownload {

    public String run(String apikey,String link){
             String apiUrl = "https://api.zenrows.com/v1/?apikey="+apikey+"&url="+link;

        try {
            String response = Request.get(apiUrl).execute().returnContent().asString();
            return response;
        } catch (Exception var4) {
            var4.printStackTrace();
            return null;
        }
    }
    public static void main(String[] args ){
        String apikey=args[0];
        String link = args[1];
        StartDownload startDownload=new StartDownload();
        String result = startDownload.run(apikey,link);
        System.out.println(result);
    }
}