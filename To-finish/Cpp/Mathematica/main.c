#include <stdio.h>
#include <string.h>

unsigned int f1(unsigned int x, unsigned int y, unsigned int z) {
    return (x + y) * z;
}

char* genPassword(char *str, unsigned int hash) {
    int byteIndex = strlen(str) - 1;
    while (byteIndex >= 0) {
        hash = f1(hash, str[byteIndex], 0x105C3);
        byteIndex--;
    }

    unsigned int n1 = 0;
    while (f1(f1(hash, n1 & 0xFF, 0x105C3), n1 >> 8, 0x105C3) != 0xA5B6) {
        if (++n1 >= 0xFFFF) {
            return "Error";
        }
    }
    n1 = (((n1 + 0x72FA) & 0xFFFF) * 99999.0 / 0xFFFF);
    char n1str[6];
    sprintf(n1str, "%05d", n1);

    int temp = atoi(n1str + 0) * 10000 + atoi(n1str + 3);
    temp = (temp / 99999.0) * 0xFFFF;
    temp = f1(f1(0, temp & 0xFF, 0x1064B), temp >> 8, 0x1064B);

    byteIndex = strlen(str) - 1;
    while (byteIndex >= 0) {
        temp = f1(temp, str[byteIndex], 0x1064B);
        byteIndex--;
    }

    unsigned int n2 = 0;
    while (f1(f1(temp, n2 & 0xFF, 0x1064B), n2 >> 8, 0x1064B) != 0xA5B6) {
        if (++n2 >= 0xFFFF) {
            return "Error";
        }
    }
    n2 = (n2 & 0xFFFF) * 99999.0 / 0xFFFF;
    char n2str[6];
    sprintf(n2str, "%05d", n2);

    static char result[16];
    sprintf(result, "%c%c%c%c-%c%c-%c%c%c::1", n2str[3], n1str[3], n1str[1], n1str[0], n2str[4], n1str[2], n2str[0], n2str[2], n1str[4], n2str[1]);

    return result;
}

int checkMathId(char *s) {
    if (strlen(s) != 16)
        return 0;
    int i = 0;
    for ( ; i < 16; i++) {
        if (i == 4 || i == 10) {
            if (s[i] != '-')
                return 0;
        } else {
            if (s[i] < '0' || s[i] > '9')
                return 0;
        }
    }
    return 1;
}

char* genActivationKey() {
    static char s[18];
    s[0] = '\0';
    int i = 0;
    for ( ; i < 14; i++) {
        char num[2];
        sprintf(num, "%d", rand() % 10);
        strcat(s, num);
        if (i == 3 || i == 7)
            strcat(s, "-");
    }
    return s;
}

int main() {
    char mathId[17];
    scanf("%16s", mathId);
    
    if (!checkMathId(mathId)) {
        printf("Bad MathID!\n");
    } else {
        char activationKey[18];
        strcpy(activationKey, genActivationKey());
        
        unsigned int magicNumbers[] = {10690, 12251, 17649, 24816, 33360, 35944, 36412, 42041, 42635, 44011, 53799, 56181, 58536, 59222, 61041};
        int numMagicNumbers = sizeof(magicNumbers) / sizeof(magicNumbers[0]);

        char software[6];
        scanf("%5s", software);

        unsigned int magicNumber;
        if (strcmp(software, "mma12") == 0 || strcmp(software, "mma13") == 0) {
            magicNumber = magicNumbers[rand() % numMagicNumbers];
        } else if (strcmp(software, "sm12") == 0) {
            unsigned int newMagicNumbers[] = {4912, 4961, 22384, 24968, 30046, 31889, 42446, 43787, 48967, 61182, 62774};
            magicNumber = newMagicNumbers[rand() % (sizeof(newMagicNumbers) / sizeof(newMagicNumbers[0]))];
        } else {
            printf("<p>Unknown software suite: %s.</p>\n", software);
            return 1;
        }

        char *password = genPassword(strcat(mathId, "$1&"), magicNumber);
		printf("Activation Key: %s\nPassword: %s\n\nThanks for using! Please consider purchasing the software if you find it helpful to you. We support genuine software.\n", activationKey, password);
	}

	scanf("%d");

    return 0;
}

