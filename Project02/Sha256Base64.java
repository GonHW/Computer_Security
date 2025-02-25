import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;

public class Sha256Base64 {

    public static void main(String[] args) {
        try {
            // Input string
            String inputString = "Hello, world!";
            
            // Create MessageDigest instance for SHA-256
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            
            // Perform the hashing
            byte[] encodedhash = digest.digest(inputString.getBytes());
            
            // Encode the hash into Base64
            String base64Hash = Base64.getEncoder().encodeToString(encodedhash);
            
            System.out.println("Input text: " + inputString);
            // Print the Base64 encoded SHA-256 hash
            System.out.println("Base64 Encoded SHA256 Hash: " + base64Hash);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
    }
}

