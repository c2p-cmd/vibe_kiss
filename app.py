# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy==2.4.2",
#     "plotly==6.5.2",
#     "scipy==1.17.0",
# ]
# ///

import marimo

__generated_with = "0.19.9"
app = marimo.App(width="full", app_title="Vibe Kiss 💋")


@app.cell
def _():
    import marimo as mo
    import base64, io, numpy as np
    from scipy.io import wavfile

    return base64, io, mo, np, wavfile


@app.cell
def _(base64, io, np, wavfile):
    def generate_kiss_sound():
        sample_rate = 44100
        duration = 0.6  # seconds

        # Create a kiss sound using noise burst and frequency sweep
        t = np.linspace(0, duration, int(sample_rate * duration))

        # Quick pop sound (initial contact)
        pop = np.random.normal(0, 0.3, int(sample_rate * 0.1))
        pop_env = np.exp(-20 * np.linspace(0, 1, len(pop)))
        pop = pop * pop_env

        # Smack/suction sound (main part)
        freq_sweep = np.linspace(800, 200, len(t))
        smack = np.sin(2 * np.pi * freq_sweep * t)
        noise = np.random.normal(0, 0.2, len(t))
        smack = 0.7 * smack + 0.3 * noise

        # Envelope for natural sound
        envelope = np.exp(-5 * t)
        smack = smack * envelope

        # Combine and pad pop at the start
        sound = np.concatenate([pop, smack[: len(smack) - len(pop)]])

        # Normalize
        sound = sound / np.max(np.abs(sound)) * 0.8
        sound = (sound * 32767).astype(np.int16)

        # Convert to base64 for embedding
        buffer = io.BytesIO()
        wavfile.write(buffer, sample_rate, sound)
        buffer.seek(0)
        audio_base64 = base64.b64encode(buffer.read()).decode()
        return f"data:audio/wav;base64,{audio_base64}"

    kiss_sound_data = generate_kiss_sound()
    return (kiss_sound_data,)


@app.cell
def _(mo):
    # Use run_button instead of regular button
    kiss_button = mo.ui.run_button(label="💋 Start Kiss Animation")
    mute_toggle = mo.ui.checkbox(label="🔇 Mute Audio", value=False)

    mo.vstack(
        [
            mo.md("# 💋 Vibe Kiss Application"),
            mo.md("Click the button to start the kissing animation with sound!"),
            mo.hstack([kiss_button, mute_toggle], justify="center"),
        ]
    )
    return kiss_button, mute_toggle


@app.cell
def _(kiss_button, kiss_sound_data, mo, mute_toggle):
    from uuid import uuid4

    # This cell only runs when kiss_button is clicked
    mo.stop(not kiss_button.value)

    should_play = not mute_toggle.value

    animation_html = f"""
    <div id='{uuid4()}'>
    <div style="text-align: center; padding: 20px;">
        <div id="kiss-animation" style="font-size: 100px; position: relative; height: 150px;">
            <span style="position: absolute; left: 20%; animation: kiss-left 2s ease-in-out;">😘</span>
            <span style="position: absolute; right: 20%; animation: kiss-right 2s ease-in-out;">😘</span>
            <span style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); opacity: 0; animation: hearts-appear 2s ease-in-out;">💕✨💖</span>
        </div>
        <div style="margin-top: 20px; font-size: 24px; color: #ff69b4; opacity: 0; animation: text-appear 2s ease-in-out;">
            *MWAH* 💋
        </div>
    </div>

    <audio id="kiss-audio" {"autoplay" if should_play else ""}>
        <source src="{kiss_sound_data}" type="audio/wav">
    </audio>

    <style>
        @keyframes kiss-left {{
            0% {{ left: 20%; transform: scale(1); }}
            50% {{ left: 45%; transform: scale(1.2); }}
            100% {{ left: 20%; transform: scale(1); }}
        }}

        @keyframes kiss-right {{
            0% {{ right: 20%; transform: scale(1) scaleX(-1); }}
            50% {{ right: 45%; transform: scale(1.2) scaleX(-1); }}
            100% {{ right: 20%; transform: scale(1) scaleX(-1); }}
        }}

        @keyframes hearts-appear {{
            0% {{ opacity: 0; transform: translate(-50%, -50%) scale(0); }}
            50% {{ opacity: 1; transform: translate(-50%, -50%) scale(1.5); }}
            100% {{ opacity: 0; transform: translate(-50%, -80%) scale(1); }}
        }}

        @keyframes text-appear {{
            0% {{ opacity: 0; transform: translateY(20px); }}
            50% {{ opacity: 1; transform: translateY(0); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
    </div>
    """

    mo.Html(animation_html)
    return


@app.cell
def _():
    import plotly.graph_objects as go

    return (go,)


@app.cell
def _(go, mo):
    de = [52.5108181, 13.3123224]
    _in = [18.5646808, 73.8322944]

    center_lat = (de[0] + _in[0]) / 2
    center_lon = (de[1] + _in[1]) / 2

    fig = go.Figure(
        go.Scattermap(
            lat=[de[0], _in[0]],
            lon=[de[1], _in[1]],
            marker={"size": 10, "color": "#0345fc"},
            text=["S", "E"],
            mode="markers+text",
            textposition="top center",
            textfont=dict(size=24),
        )
    )

    fig.update_layout(
        map={
            "style": "open-street-map",
            "center": {"lat": center_lat, "lon": center_lon},
            "zoom": 1,
        },
        showlegend=False,
    )

    mo.md("## 🌍 From Berlin to India with Love 💖")
    return (fig,)


@app.cell
def _(mo):
    pass_field = mo.ui.text(
        kind="password", 
        placeholder="My nickname for you",
        label="Enter Password to Reveal the Secret Message",
        full_width=True
    )
    pass_field
    return (pass_field,)


@app.cell
def _(mo, pass_field):
    msg = ""
    _value = pass_field.value
    if _value == 'Chinku':
        msg = "Jaha bhi ho, jaisi bhi ho, hamesha yaad rakhna, meri ho ♥️"
    elif len(_value) > 0:
        msg = "Incorrect password. Try again! Hint: It's a cute nickname."
    mo.md(msg)
    return


@app.cell
def _(fig, mo):
    mo.Html(
        f"""
    <div style="
        width: 800px;
        aspect-ratio: 1;
        clip-path: polygon(-41% 0, 50% 91%, 141% 0);
        background: 
            radial-gradient(at 70% 31%, #ffe0f0 29%, transparent 30%),
            radial-gradient(at 30% 31%, #ffe0f0 29%, transparent 30%),
            linear-gradient(#ffe0f0 0 0) bottom/100% 50% no-repeat;
        offset-position: bottom 30px;
        margin: 40px auto;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    ">
        {mo.ui.plotly(fig)}
    </div>
    """
    )
    return


if __name__ == "__main__":
    app.run()
