#include <cstdio>

#include "mixer.h"

int main() {
    Mixer* mixer = new Mixer();
    mixer->addVoice("door", 3.0f, 4.0f, 0.0f, 2.0f, 1.0f);
    mixer->addVoice("torch", 0.0f, 0.0f, 0.0f, 0.0f, 0.5f);
    mixer->addVoice("guard", 12.5f, -7.25f, 1.75f, 4.0f, 0.8f);
    mixer->addVoice("clock", 101.3f, 0.0f, 0.0f, 1.0f, 1.0f);
    mixer->report();

    Samples block;
    for (int i = 0; i < 1000; ++i) block.push_back(0.001f * (float)(i % 17) + 0.1f);
    std::printf("energy=%.9g\n", mixer->blockEnergy(block));
    std::printf("mix=%.9g\n", mixer->mix(block.data(), (int)block.size()));

    Voice* found = NULL;
    if (mixer->findVoice("guard", &found)) std::printf("found %s\n", found->name.c_str());
    if (!mixer->findVoice("bell", &found)) std::printf("no bell\n");
    std::printf("has door=%d bell=%d\n", mixer->hasVoice("door"), mixer->hasVoice("bell"));

    std::vector<int> events;
    events.push_back(16);
    events.push_back(5);
    mixer->spreadEvents(events);
    for (size_t i = 0; i < events.size(); ++i) std::printf("%d ", events[i]);
    std::printf("\n");

    delete mixer;
}
