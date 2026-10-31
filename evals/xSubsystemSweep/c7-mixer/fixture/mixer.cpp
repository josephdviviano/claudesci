#include "mixer.h"

#include <cmath>
#include <cstdio>

#define MAX_VOICES 8
#define SPEED_OF_SOUND 343.2

Bus::~Bus() { std::printf("close %s total=%.9g\n", label_, total_); }

Mixer::Mixer() : musicBus(new Bus("music")), sfxBus(new Bus("sfx")) {}

Mixer::~Mixer() {
    for (size_t i = 0; i < voices.size(); ++i) delete voices[i];
    delete musicBus;
    delete sfxBus;
}

bool Mixer::addVoice(const char* name, float x, float y, float z, float gain, float sensitivity) {
    if (voices.size() >= MAX_VOICES) return false;
    Voice* v = new Voice();
    v->name = name;
    v->position[0] = x;
    v->position[1] = y;
    v->position[2] = z;
    v->gain = gain;
    v->filter = new Filter(0.5f);
    Listener* l = (Listener*)v;
    l->sensitivity = sensitivity;
    slotByName[name] = (int)voices.size();
    voices.push_back(v);
    return true;
}

bool Mixer::findVoice(const std::string& name, Voice** out) const {
    std::map<std::string, int>::const_iterator it = slotByName.find(name);
    if (it == slotByName.end()) return false;
    *out = voices[it->second];
    return true;
}

bool Mixer::hasVoice(const std::string& name) const {
    return slotByName.find(name) != slotByName.end();
}

float Mixer::attenuate(const Voice& v) const {
    float d = std::sqrt(v.position[0] * v.position[0] + v.position[1] * v.position[1] +
                        v.position[2] * v.position[2]);
    float raw = v.gain * v.sensitivity / d;
    return raw < 1.0f ? raw : 1.0f;
}

float Mixer::delaySeconds(const Voice& v) const {
    float d = std::sqrt(v.position[0] * v.position[0] + v.position[1] * v.position[1] +
                        v.position[2] * v.position[2]);
    return d / SPEED_OF_SOUND;
}

float Mixer::blockEnergy(const Samples& block) const {
    double total = 0;
    for (size_t i = 0; i < block.size(); ++i) total += block[i] * block[i];
    return (float)total;
}

float Mixer::mix(const float* input, int count) {
    float out = 0.0f;
    for (int i = 0; i < count; ++i) {
        for (size_t j = 0; j < voices.size(); ++j) {
            Voice* v = voices[j];
            out += v->filter->process(input[i] * attenuate(*v));
        }
    }
    sfxBus->send(out);
    musicBus->send(out * 0.5f);
    return out;
}

void Mixer::spreadEvents(std::vector<int>& events) const {
    for (size_t i = 0; i < events.size(); ++i) {
        if (events[i] > 1) events.push_back(events[i] / 2);
    }
}

void Mixer::report() const {
    for (std::map<std::string, int>::const_iterator it = slotByName.begin(); it != slotByName.end();
         ++it) {
        const Voice* v = voices[it->second];
        std::printf("%s slot=%d gain=%.9g delay=%.9g sens=%.9g\n", it->first.c_str(), it->second,
                    attenuate(*v), delaySeconds(*v), v->sensitivity);
    }
}
