from gym.envs.registration import register

register(
    id='roomba-v0',
    entry_point='roomba_env.envs:RoombaEnv',
)