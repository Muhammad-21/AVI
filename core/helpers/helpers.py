def white_color_by_mode(mode):
    if mode == '1':
        return 1
    if mode == 'L':
        return 255
    if mode == 'RGB':
        return 255, 255, 255

    raise ValueError(f'Mode {mode} is unsupported')
