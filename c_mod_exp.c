#include <stdio.h>
#include <gmp.h>
#include <string.h>


void append(char* s, char c)
{
        int len = strlen(s);
        s[len] = c;
        s[len+1] = '\0';
}

void bits_of_n(char bits[],mpz_t n){
    mpz_t r,d;
    mpz_init(r);
    mpz_init(d);

    mpz_set_str(d, "2", 10);
    while(mpz_cmp_si(n,0)){
        append(bits,char(int('0') + mpz_fdiv_ui(n,2)));
        mpz_fdiv_q(r,n,d);
        n = r;
    }
}

void reverse(char str[]){
    int i,j;
    char temp[100];
    for(i=strlen(str)-1,j=0; i+1!=0; --i,++j)
    {
        temp[j]=str[i];
    }
    temp[j]='\0';
    strcpy(str,temp);
}

void mod_exp(mpz_t result, mpz_t x,mpz_t n,mpz_t m){
    mpz_set_str(result, "1", 10);

    char bits[] = "";
    bits_of_n(bits, n);

    reverse(bits);
    size_t str_size = strlen(bits);

    for(int i=0; i<str_size; i++){
        mpz_mul(result, result, result);
        mpz_mod(result, result, m);

        if(bits[i]=='1'){
            mpz_mul(result, result, x);
            mpz_mod(result, result, m);
        }
    }
}

int main(int argc, char* argv[]){

    char input[] = "";
    mpz_t x,n,m,integ,result;
    mpz_init(integ);
    mpz_init(x);
    mpz_init(n);
    mpz_init(m);
    mpz_init(result);

    mpz_set_str(x, argv[1], 10);
    mpz_set_str(n, argv[2], 10);
    mpz_set_str(m, argv[3], 10);
    mod_exp(result, x, n, m);
    mpz_out_str(stdout, 10, result);
    return 0;
}
