package com;

import io.appium.java_client.android.AndroidDriver;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.remote.DesiredCapabilities;

import java.io.*;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class StartInstall {

    public static AndroidDriver setUp(String uid,URL URL) throws MalformedURLException {


        DesiredCapabilities capabilities = new DesiredCapabilities();
        capabilities.setCapability("platformName","Android");
        capabilities.setCapability("deviceName",uid);

        capabilities.setCapability("newCommandTimeout", 6000);

        AndroidDriver driver = new AndroidDriver(URL, capabilities);
        driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
        return driver;

    }
    public static void clickButton(AndroidDriver driver){
        String installID="android:id/button1";
        WebElement element = driver.findElement(By.id(installID));
        element.click();

    }

    public static boolean  intall(String PATH, String uid, String url) throws InterruptedException, IOException {
        boolean result = false;
        AndroidDriver driver ;
        try {
            List<String> output = new ArrayList<>();
            driver = setUp(uid, new URL(url));
            File directory = new File(PATH);
            String[] apks = directory.list(new ApkFilter());
            for (int i = 0; i < apks.length; i++) {
            String cmd = String.format("adb -s %s install \"%s\"",uid,PATH);
            Runtime rt = Runtime.getRuntime();
            Process proc = rt.exec(cmd);
            Thread.sleep(5000L);
            clickButton(driver);
            clickButton(driver);
            InputStream stdin = proc.getInputStream();
            InputStreamReader isr = new InputStreamReader(stdin);
            BufferedReader br = new BufferedReader(isr);
            String line = null;
            while ((line = br.readLine()) != null) {
                output.add(line);

            }

            for (int j=0;output!=null&&j<output.size();j++){
                String tmpStr=output.get(j);
                if(tmpStr!=null&&tmpStr.contains("Success")) {
                    result=true;

                }
            }
            }
        } catch (MalformedURLException e) {

            result = false;

        }


        return result;
    }
    static class ApkFilter implements FilenameFilter {

        public boolean isApk(String file) {
            if (file.toLowerCase().endsWith(".apk")) {
                return true;
            } else {
                return false;
            }
        }

        @Override
        public boolean accept(File dir, String name) {
            return isApk(name);
        }
    }

    public static void main(String[] args ) throws IOException, InterruptedException {
        String PATH=args[0];
        String uid = args[1];
        String url=args[2];

        Boolean install=intall(PATH,uid,url);
        System.out.println(install);

    }

}
