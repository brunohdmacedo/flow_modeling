def main(nt, p_it, freq):
    import numpy as np
    import gc
    import os
    import time
    import shutil

    from script.navier_stokes import navier_stokes
    from script.channel_shape import channel_shape
    from script.plot_gif import plot_gif
    import params_channel_shape
    import params_to_calc
    
    dx = params_to_calc.dx
    dy = params_to_calc.dy

    dt = params_to_calc.dt

    rho = params_to_calc.rho
    nu = params_to_calc.nu
    D = params_to_calc.D

    F = params_to_calc.F
    P0 = params_to_calc.P0
    
    nx = params_channel_shape.nx
    ny = params_channel_shape.ny

    field = params_channel_shape.field
    anode_value = params_channel_shape.anode_value
    cathode_value = params_channel_shape.cathode_value
    border_value = params_channel_shape.border_value
    w = params_channel_shape.w
    h = params_channel_shape.h
    d = params_channel_shape.d
    s = params_channel_shape.s
    bottom_left = params_channel_shape.bottom_left
    top_left = params_channel_shape.top_left
    bottom_right = params_channel_shape.bottom_right

    v = params_channel_shape.v
    u = params_channel_shape.u
    p = params_channel_shape.p
    b = params_channel_shape.b

    
    

    try:
        
        n_save = nt // 200 if nt > 200 else 1
        save_folder = './results/'
        save_folder += time.strftime('%Y_%m_%d_%H_%M', time.localtime())
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
            
        u, v, p = navier_stokes(u, v, freq,
                          w, h, d, s,
                          bottom_left, top_left, bottom_right,
                          anode_value, cathode_value,
                          border_value,
                          ny, nx,
                          p, b,
                          rho, nu, 
                          dt, dx, dy,
                          F, P0, nt, n_save, p_it, save_folder=save_folder)
        
        p_gif = channel_shape(field = field,
                          w=w, h=h, d=d, s=s,
                          bottom_left=bottom_left, top_left=top_left,
                          bottom_right=bottom_right,
                          anode_value=anode_value+10000, cathode_value=cathode_value+10000,
                          border_value=border_value+10000, nx=nx,
                          ny=ny)
        
        np.save(save_folder + '/' + 'channel_for_gif', p)
        
        names = ['p_init_0', 'u_init_0', 'v_init_0']
        files = ['p_gr.npy', 'u_gr.npy', 'v_gr.npy']
        ch_it = np.load(save_folder + '/ch_it.npy').tolist()
        
        for file, name in zip(files, names):
            gc.collect()
            imgs = np.load(save_folder + '/' + file)
            vmin, vmax = np.mean(imgs[imgs<0]), np.mean(imgs[imgs>0])
            mean = np.mean(np.abs([vmin, vmax]))
            vmin, vmax = -mean, mean
            if vmax > 0.2:
                vmin, vmax = -0.02, 0.02
            plot_gif(imgs, p_gif, name, vmin, vmax, ch_it, save_folder)
            gc.collect()
            print(f'Gif {name} was saved')
        
        shutil.copy('params_to_calc.py', save_folder)
        shutil.copy('params_channel_shape.py', save_folder)
        print('Params was saved')
        print(f'Directory name: {save_folder}')
        
        
        
        gc.collect()
    except KeyboardInterrupt:
        os.rmdir(save_folder)
        print(f'\nNothing to save! Folder {save_folder} was removed')
        
if __name__ == '__main__':
    
    import argparse
    
    nt = 20
    p_it = 1000
    freq = .1
    
    parser = argparse.ArgumentParser(description='Create params for calculation')
    parser.add_argument('--nt', default=nt, type=int)
    parser.add_argument('--p_it', default=p_it, type=int)
    parser.add_argument('--freq', default=freq, type=float)
    
    args = parser.parse_args()
    main(nt=args.nt, p_it=args.p_it, freq=args.freq)