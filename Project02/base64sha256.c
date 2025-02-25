#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/evp.h>

// Function to perform Base64 encoding
static const char encodingTable[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
static const int modTable[] = {0, 2, 1};

char* base64_encode(const unsigned char *data, size_t inputLength, size_t *outputLength) {
    *outputLength = 4 * ((inputLength + 2) / 3);
    char *encodedData = malloc(*outputLength);
    if (encodedData == NULL) return NULL;

    for (int i = 0, j = 0; i < inputLength;) {
        uint32_t octet_a = i < inputLength ? (unsigned char)data[i++] : 0;
        uint32_t octet_b = i < inputLength ? (unsigned char)data[i++] : 0;
        uint32_t octet_c = i < inputLength ? (unsigned char)data[i++] : 0;

        uint32_t triple = (octet_a << 0x10) + (octet_b << 0x08) + octet_c;

        encodedData[j++] = encodingTable[(triple >> 3 * 6) & 0x3f];
        encodedData[j++] = encodingTable[(triple >> 2 * 6) & 0x3f];
        encodedData[j++] = encodingTable[(triple >> 1 * 6) & 0x3f];
        encodedData[j++] = encodingTable[(triple >> 0 * 6) & 0x3f];
    }

    for (int i = 0; i < modTable[inputLength % 3]; i++)
        encodedData[*outputLength - 1 - i] = '=';
    
    encodedData[*outputLength] = 0;
    return encodedData;
}

int main() {
    // Initialize OpenSSL algorithms
    OpenSSL_add_all_algorithms();

    // Input string
    char input_text[] = "Hello, world!";
    unsigned char hash[EVP_MAX_MD_SIZE]; // Buffer for the hash
    unsigned int hash_len;

    // Create and initialize the context
    EVP_MD_CTX* ctx = EVP_MD_CTX_new();
    EVP_DigestInit_ex(ctx, EVP_sha256(), NULL);
    EVP_DigestUpdate(ctx, input_text, strlen(input_text));
    EVP_DigestFinal_ex(ctx, hash, &hash_len);
    
    // Base64 encode the SHA256 hash
    size_t outputLength;
    char *base64_string = base64_encode(hash, hash_len, &outputLength);

    printf("Input text: %s\n", input_text);
    // Print the Base64 encoded SHA256 hash
    printf("Base64 Encoded SHA256 Hash: %s\n", base64_string);

    // Clean up
    EVP_MD_CTX_free(ctx);
    free(base64_string);
    EVP_cleanup(); // Clean up the OpenSSL algorithms library

    return 0;
}

