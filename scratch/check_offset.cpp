#include <stdio.h>
#include <stddef.h>
#include "Player.hpp"

int main() {
    printf("Player::laserTimer = 0x%zx\n", offsetof(th06::Player, laserTimer));
    printf("Player::focusMovementTimer = 0x%zx\n", offsetof(th06::Player, focusMovementTimer));
    printf("Player::bullets = 0x%zx\n", offsetof(th06::Player, bullets));
    return 0;
}
