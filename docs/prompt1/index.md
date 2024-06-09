# Project Title

## Initial Prompt
![Initial Prompt Waveform](initial_prompt/initial_prompt_waveform_spectrogram.png)
<audio controls>
  <source src="initial_prompt/initial_prompt.wav" type="audio/wav">
Your browser does not support the audio element.
</audio>

## Stem Content

### Vocals
![Vocals Waveform](stem/vocals_waveform_spectrogram.png)
<audio controls>
  <source src="stem/vocals.wav" type="audio/wav">
Your browser does not support the audio element.
</audio>

### Bass
![Bass Waveform](stem/bass_waveform_spectrogram.png)
<audio controls>
  <source src="stem/bass.wav" type="audio/wav">
Your browser does not support the audio element.
</audio>

### Drums
![Drums Waveform](stem/drums_waveform_spectrogram.png)
<audio controls>
  <source src="stem/drums.wav" type="audio/wav">
Your browser does not support the audio element.
</audio>

### Other
![Other Waveform](stem/other_waveform_spectrogram.png)
<audio controls>
  <source src="stem/other.wav" type="audio/wav">
Your browser does not support the audio element.
</audio>

## Iterations

### Drums Iterations
{% for i in (1..10) %}
#### Drums Iteration {{i}}
![Drums {{i}} Waveform](iterations/drums_{{i}}_waveform_spectrogram.png)
<audio controls>
  <source src="iterations/drums_{{i}}.wav" type="audio/wav">
Your browser does not support the audio element.
</audio>
{% endfor %}

### Bass Iterations
{% for i in (1..10) %}
#### Bass Iteration {{i}}
![Bass {{i}} Waveform](iterations/bass_{{i}}_waveform_spectrogram.png)
<audio controls>
  <source src="iterations/bass_{{i}}.wav" type="audio/wav">
Your browser does not support the audio element.
</audio>
{% endfor %}

### Vocals Iterations
{% for i in (1..10) %}
#### Vocals Iteration {{i}}
![Vocals {{i}} Waveform](iterations/vocals_{{i}}_waveform_spectrogram.png)
<audio controls>
  <source src="iterations/vocals_{{i}}.wav" type="audio/wav">
Your browser does not support the audio element.
</audio>
{% endfor %}

### Other Iterations
{% for i in (1..10) %}
#### Other Iteration {{i}}
![Other {{i}} Waveform](iterations/other_{{i}}_waveform_spectrogram.png)
<audio controls>
  <source src="iterations/other_{{i}}.wav" type="audio/wav">
Your browser does not support the audio element.
</audio>
{% endfor %}
