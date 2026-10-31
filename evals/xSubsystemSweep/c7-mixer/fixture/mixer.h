#pragma once

#include <map>
#include <string>
#include <vector>

typedef std::vector<float> Samples;

struct Named {
    virtual ~Named() = default;
    std::string name;
};

struct Listener {
    virtual ~Listener() = default;
    float sensitivity = 1.0f;
};

class Filter {
public:
    explicit Filter(float cutoff) : cutoff_(cutoff) {}
    float process(float in) {
        state_ += cutoff_ * (in - state_);
        return state_;
    }

private:
    float cutoff_;
    float state_ = 0.0f;
};

struct Voice : Named, Listener {
    Voice() : filter(NULL) {}
    ~Voice() { delete filter; }
    Voice(const Voice&) = delete;
    Voice& operator=(const Voice&) = delete;

    float position[3];
    float gain = 0.0f;
    Filter* filter;
};

class Bus {
public:
    explicit Bus(const char* label) : label_(label) {}
    ~Bus();
    void send(float level) { total_ += level; }
    float total() const { return total_; }

private:
    const char* label_;
    float total_ = 0.0f;
};

class Mixer {
public:
    Mixer();
    ~Mixer();
    bool addVoice(const char* name, float x, float y, float z, float gain, float sensitivity);
    bool findVoice(const std::string& name, Voice** out) const;
    bool hasVoice(const std::string& name) const;
    float attenuate(const Voice& v) const;
    float delaySeconds(const Voice& v) const;
    float blockEnergy(const Samples& block) const;
    float mix(const float* input, int count);
    void spreadEvents(std::vector<int>& events) const;
    void report() const;

private:
    Bus* musicBus;
    Bus* sfxBus;
    std::vector<Voice*> voices;
    std::map<std::string, int> slotByName;
};
