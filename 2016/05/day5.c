#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <openssl/evp.h>

#ifndef MD5_DIGEST_LENGTH
#define MD5_DIGEST_LENGTH 16
#endif
#define MAX_DIGITS_UINT64 20

const EVP_MD *md;

void md5(const char *s, size_t len, unsigned char *hash)
{
	EVP_MD_CTX *mdctx = EVP_MD_CTX_new();
	unsigned int md_len;

	EVP_DigestInit_ex(mdctx, md, NULL);
	EVP_DigestUpdate(mdctx, s, len);
	EVP_DigestFinal_ex(mdctx, hash, &md_len);
	EVP_MD_CTX_free(mdctx);
}

void print_md5(unsigned char *hash)
{
	int i;

	for (i = 0; i < MD5_DIGEST_LENGTH; i++)
		printf("%02x", hash[i]);
	printf("\n");
}

//#define INPUT "abc"
#define INPUT "ffykfhsq"

int count_marked(int *marked)
{
	int i;
	int sum = 0;

	for (i = 0; i < 8; i++)
		sum += marked[i];

	return sum;
}

int main(void)
{
	unsigned char hash[MD5_DIGEST_LENGTH];
	char buf[MAX_DIGITS_UINT64 + 10];
	int part2[8] = { 0, 0, 0, 0, 0, 0, 0, 0 };
	int marked[8] = { 0, 0, 0, 0, 0, 0, 0, 0 };
	uint64_t i;
	int found = 0;


	memset(part2, 0, 9);
	OpenSSL_add_all_digests();
	md = EVP_get_digestbyname("md5");

	printf("part 1: ");
	for (i = 0; i < 99999999999999999; i++)
	{
		int index;
		snprintf(buf, sizeof(buf), INPUT "%llu", i);
		md5(buf, strlen(buf), hash);
		if (hash[0] == 0 && hash[1] == 0 && (hash[2] & 0xf0) == 0) {
			if (found < 8) {
				printf("%x", hash[2] & 0x0f);
				fflush(stdout);
				found++;
			}
			index = hash[2] & 0x0f;
			if (index < 8 && marked[index] == 0) {
				marked[index] = 1;
				part2[index] = hash[3] >> 4;
			}

			if (count_marked(marked) == 8)
				break;
		}
	}

	printf("\npart 2: ");
	for (i = 0; i < 8; i++)
		printf("%x", part2[i]);
	printf("\n");

	EVP_cleanup();

	return 0;
}
