import pathlib
import shutil
import subprocess
import sys
import tempfile

FIXTURE = pathlib.Path(sys.argv[1])

REWRITES = {
    "S1 typedef->using": [
        ("mixer.h", "typedef std::vector<float> Samples;", "using Samples = std::vector<float>;"),
    ],
    "S2 NULL->nullptr": [
        ("mixer.h", "filter(NULL)", "filter(nullptr)"),
    ],
    "S3 #define int->constexpr": [
        ("mixer.cpp", "#define MAX_VOICES 8", "constexpr size_t MAX_VOICES = 8;"),
    ],
    "S4 C array->std::array": [
        ("mixer.h", "#include <map>", "#include <array>\n#include <map>"),
        ("mixer.h", "float position[3];", "std::array<float, 3> position;"),
    ],
    "S5 Voice::filter->unique_ptr": [
        ("mixer.h", "#include <map>", "#include <map>\n#include <memory>"),
        ("mixer.h", "    Voice() : filter(NULL) {}\n    ~Voice() { delete filter; }\n", "    Voice() = default;\n"),
        ("mixer.h", "    Filter* filter;", "    std::unique_ptr<Filter> filter;"),
        ("mixer.cpp", "v->filter = new Filter(0.5f);", "v->filter = std::make_unique<Filter>(0.5f);"),
    ],
    "S6 find!=end->contains": [
        ("mixer.cpp", "return slotByName.find(name) != slotByName.end();", "return slotByName.contains(name);"),
    ],
    "S7 out-param->return pointer": [
        ("mixer.h", "bool findVoice(const std::string& name, Voice** out) const;", "Voice* findVoice(const std::string& name) const;"),
        ("mixer.cpp",
         "bool Mixer::findVoice(const std::string& name, Voice** out) const {\n"
         "    std::map<std::string, int>::const_iterator it = slotByName.find(name);\n"
         "    if (it == slotByName.end()) return false;\n"
         "    *out = voices[it->second];\n"
         "    return true;\n}",
         "Voice* Mixer::findVoice(const std::string& name) const {\n"
         "    auto it = slotByName.find(name);\n"
         "    return it == slotByName.end() ? nullptr : voices[it->second];\n}"),
        ("main.cpp",
         '    Voice* found = NULL;\n'
         '    if (mixer->findVoice("guard", &found)) std::printf("found %s\\n", found->name.c_str());\n'
         '    if (!mixer->findVoice("bell", &found)) std::printf("no bell\\n");',
         '    if (Voice* found = mixer->findVoice("guard")) std::printf("found %s\\n", found->name.c_str());\n'
         '    if (!mixer->findVoice("bell")) std::printf("no bell\\n");'),
    ],
    "S8 index loop->range-for": [
        ("mixer.cpp",
         "        for (size_t j = 0; j < voices.size(); ++j) {\n            Voice* v = voices[j];\n",
         "        for (Voice* v : voices) {\n"),
    ],
    "S9 iterator .first/.second->structured bindings": [
        ("mixer.cpp",
         "    for (std::map<std::string, int>::const_iterator it = slotByName.begin(); it != slotByName.end();\n"
         "         ++it) {\n"
         "        const Voice* v = voices[it->second];\n"
         '        std::printf("%s slot=%d gain=%.9g delay=%.9g sens=%.9g\\n", it->first.c_str(), it->second,',
         "    for (const auto& [name, slot] : slotByName) {\n"
         "        const Voice* v = voices[slot];\n"
         '        std::printf("%s slot=%d gain=%.9g delay=%.9g sens=%.9g\\n", name.c_str(), slot,'),
    ],
    "S10 C-style int cast->static_cast": [
        ("mixer.cpp", "(int)voices.size()", "static_cast<int>(voices.size())"),
    ],
    "S11 pointer+length->span": [
        ("mixer.h", "#include <map>", "#include <map>\n#include <span>"),
        ("mixer.h", "float mix(const float* input, int count);", "float mix(std::span<const float> input);"),
        ("mixer.cpp", "float Mixer::mix(const float* input, int count) {", "float Mixer::mix(std::span<const float> input) {"),
        ("mixer.cpp", "    for (int i = 0; i < count; ++i) {", "    for (float sample : input) {"),
        ("mixer.cpp", "input[i] * attenuate", "sample * attenuate"),
        ("main.cpp", "mixer->mix(block.data(), (int)block.size())", "mixer->mix(block)"),
    ],
    "S12 vector<Voice*>->vector<unique_ptr>": [
        ("mixer.h", "#include <map>", "#include <map>\n#include <memory>"),
        ("mixer.h", "std::vector<Voice*> voices;", "std::vector<std::unique_ptr<Voice>> voices;"),
        ("mixer.cpp", "    for (size_t i = 0; i < voices.size(); ++i) delete voices[i];\n", ""),
        ("mixer.cpp", "voices.push_back(v);", "voices.emplace_back(v);"),
        ("mixer.cpp", "*out = voices[it->second];", "*out = voices[it->second].get();"),
        ("mixer.cpp", "Voice* v = voices[j];", "Voice* v = voices[j].get();"),
        ("mixer.cpp", "const Voice* v = voices[it->second];", "const Voice* v = voices[it->second].get();"),
    ],
    "T1 ternary min->std::min (NaN)": [
        ("mixer.cpp", "#include <cmath>", "#include <algorithm>\n#include <cmath>"),
        ("mixer.cpp", "return raw < 1.0f ? raw : 1.0f;", "return std::min(raw, 1.0f);"),
    ],
    "T2 MI cast->reinterpret_cast": [
        ("mixer.cpp", "(Listener*)v", "reinterpret_cast<Listener*>(v)"),
    ],
    "T2 safe form: static_cast": [
        ("mixer.cpp", "(Listener*)v", "static_cast<Listener*>(v)"),
    ],
    "T3 double macro->constexpr float": [
        ("mixer.cpp", "#define SPEED_OF_SOUND 343.2", "constexpr float SPEED_OF_SOUND = 343.2f;"),
    ],
    "T3 safe form: constexpr double": [
        ("mixer.cpp", "#define SPEED_OF_SOUND 343.2", "constexpr double SPEED_OF_SOUND = 343.2;"),
    ],
    "T4 growing index loop->range-for": [
        ("mixer.cpp",
         "    for (size_t i = 0; i < events.size(); ++i) {\n        if (events[i] > 1) events.push_back(events[i] / 2);\n",
         "    for (int e : events) {\n        if (e > 1) events.push_back(e / 2);\n"),
    ],
    "T5 buses->unique_ptr": [
        ("mixer.h", "#include <map>", "#include <map>\n#include <memory>"),
        ("mixer.h", "    Bus* musicBus;\n    Bus* sfxBus;", "    std::unique_ptr<Bus> musicBus;\n    std::unique_ptr<Bus> sfxBus;"),
        ("mixer.cpp", "    delete musicBus;\n    delete sfxBus;\n", ""),
        ("mixer.cpp", "musicBus(new Bus(\"music\")), sfxBus(new Bus(\"sfx\"))", "musicBus(std::make_unique<Bus>(\"music\")), sfxBus(std::make_unique<Bus>(\"sfx\"))"),
    ],
    "T5 safe form: unique_ptr, declarations reordered": [
        ("mixer.h", "#include <map>", "#include <map>\n#include <memory>"),
        ("mixer.h", "    Bus* musicBus;\n    Bus* sfxBus;", "    std::unique_ptr<Bus> sfxBus;\n    std::unique_ptr<Bus> musicBus;"),
        ("mixer.cpp", "    delete musicBus;\n    delete sfxBus;\n", ""),
        ("mixer.cpp", "musicBus(new Bus(\"music\")), sfxBus(new Bus(\"sfx\"))", "sfxBus(std::make_unique<Bus>(\"sfx\")), musicBus(std::make_unique<Bus>(\"music\"))"),
    ],
    "T6 double sum->inner_product 0.0f": [
        ("mixer.cpp", "#include <cmath>", "#include <cmath>\n#include <numeric>"),
        ("mixer.cpp",
         "    double total = 0;\n    for (size_t i = 0; i < block.size(); ++i) total += block[i] * block[i];\n    return (float)total;",
         "    return std::inner_product(block.begin(), block.end(), block.begin(), 0.0f);"),
    ],
    "T6 safe form: inner_product 0.0": [
        ("mixer.cpp", "#include <cmath>", "#include <cmath>\n#include <numeric>"),
        ("mixer.cpp",
         "    double total = 0;\n    for (size_t i = 0; i < block.size(); ++i) total += block[i] * block[i];\n    return (float)total;",
         "    return static_cast<float>(std::inner_product(block.begin(), block.end(), block.begin(), 0.0));"),
    ],
}

for label, edits in REWRITES.items():
    work = pathlib.Path(tempfile.mkdtemp())
    for name in ("mixer.h", "mixer.cpp", "main.cpp"):
        shutil.copy(FIXTURE / name, work / name)
    for name, old, new in edits:
        text = (work / name).read_text()
        if text.count(old) != 1:
            sys.exit(f"{label}: pattern not found once in {name}: {old!r}")
        (work / name).write_text(text.replace(old, new))
    result = subprocess.run([str(FIXTURE / "check.sh"), str(work)], capture_output=True, text=True, errors="replace", timeout=60)
    status = "PASS" if result.returncode == 0 else "FAIL"
    print(f"{status}  {label}")
