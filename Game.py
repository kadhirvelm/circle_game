#!/usr/bin/env python3

from circle_game.Controller import Controller
import pygame


def main():
    print("Hello World")
    paths = Controller.return_microsoft_paths()
    player1_input = Controller(paths[0])
    player2_input = Controller(paths[1])

if __name__ == '__main__':
    main()
