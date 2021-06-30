package us.yuxin.x.ethereum.address;

import org.web3j.crypto.ECKeyPair;
import org.web3j.crypto.Keys;


import java.security.InvalidAlgorithmParameterException;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.util.Random;

public class Generator {
    public static Random random;

    static {
        random = new Random();
        random.setSeed(System.currentTimeMillis());
    }


    public static byte[] randomByteArray(int size) {
        byte[] arr = new byte[size];
        for (int i = 0; i < size; i++) {
            arr[i] = (byte)random.nextInt(0x100);
        }
        return arr;
    }



    public static void main(String ... args) {
        /*
        https://ethereum.stackexchange.com/questions/41072/generate-private-key-and-address-using-web3j
         */
        try {
            for (int i = 0; i < 1000; i++) {
                ECKeyPair ecKeyPair = Keys.createEcKeyPair();
                String privateKey = ecKeyPair.getPrivateKey().toString(16);
                String publicKey = ecKeyPair.getPublicKey().toString(16);

                System.out.println(publicKey.length());
                System.out.println(Keys.getAddress(ecKeyPair));
            }

        } catch (InvalidAlgorithmParameterException | NoSuchAlgorithmException | NoSuchProviderException e) {
            e.printStackTrace();
        }
    }
}
