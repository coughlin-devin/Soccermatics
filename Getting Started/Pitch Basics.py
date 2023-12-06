from mplsoccer.pitch import Pitch, VerticalPitch

# plot a pitch
pitch = Pitch(pitch_color='grass', line_color='white', stripe=True)
fig, ax = pitch.draw()

# plot a verticcal pitch
pitch = VerticalPitch(pitch_color='grass', line_color='white', stripe=True)
fig, ax = pitch.draw()

# plot half a pitch
half = Pitch(pitch_color='grass', line_color='white', stripe=True, half=True, corner_arcs=True)
fig, ax = half.draw()

# NOTE
# mplsoccer supports 10 pitch types by specifying the pitch_type argument:
#   ‘statsbomb’ (default), ‘opta’, ‘tracab’, ‘wyscout’, ‘uefa’, ‘metricasports’, ‘custom’, ‘skillcorner’, ‘secondspectrum’ and ‘impect’.
# If you are using tracking data or the custom pitch (‘metricasports’, ‘tracab’, ‘skillcorner’, ‘secondspectrum’ or ‘custom’),
#   you also need to specify the pitch_length and pitch_width, which are typically 105 and 68 respectively.

# NOTE
# You can also adjust the pitch orientations with the pad_left, pad_right, pad_bottom and pad_top arguments to make arbitrary pitch shapes.
pitch = VerticalPitch(half=True, pitch_color='grass', line_color='white', stripe=True,
                      pad_left=-15,  # bring the left axis in 10 data units (reduce the size)
                      pad_right=-15,  # bring the right axis in 10 data units (reduce the size)
                      pad_top=1.5,  # extend the top axis 10 data units
                      pad_bottom=-36)  # extend the bottom axis 20 data units
fig, ax = pitch.draw()

# NOTE
# The pitch line style is adjustable. Use linestyle and goal_linestyle to adjust the colors.
# The pitch transparency is adjustable. Use pitch_alpha and goal_alpha to adjust the colors.
pitch = Pitch(pitch_color='grass', line_color='white', stripe=True, linestyle='--', linewidth=1, goal_linestyle='-', line_alpha=0.5, goal_alpha=0.3)
fig, ax = pitch.draw()

# NOTE
# You can add the Juego de Posición pitch lines and shade the middle third.
# You can also adjust the transparency via shade_alpha and positional_alpha.
pitch = Pitch(pitch_color='grass', line_color='white', stripe=True, goal_type='box', positional=True, shade_middle=True, positional_linestyle='--', positional_color='white', shade_color='#d9e829')
fig, ax = pitch.draw()
