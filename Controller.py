import hid


def main():
    try:
        print("Opening the device")

        paths = []
        for d in hid.enumerate():
            if d['product_id'] == 39:
                paths.append(d['path'])

        h1 = hid.device()
        h2 = hid.device()

        h1.open_path(paths[0])
        h2.open_path(paths[1])

        print("Closing the device")
        h1.close()
        h2.close()

    except IOError as ex:
        print(ex)
        print("You probably don't have the hard coded device. Update the hid.device line")
        print("in this script with one from the enumeration list output above and try again.")


def input_translate(data):
    letter = data[2]
    if letter == 1:
        return 'A'
    elif letter == 2:
        return 'B'
    elif letter == 4:
        return 'X'
    elif letter == 8:
        return 'Y'
    elif letter == 16:
        return 'LT'
    elif letter == 32:
        return 'RT'
    elif letter == 0:
        return 'Released'
    else:
        return 'Unknown'


if __name__ == "__main__":
    main()
