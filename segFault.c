#include <stdlib.h>

void screwUp() {
  char *none;
  none = (char *) 0;
  none[0] = 'a';
}

int main(int argc, char **argv) {
  screwUp();
  return 0;
}
