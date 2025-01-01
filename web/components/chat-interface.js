const ChatInterface = {
  template: `
    <div class="chat-interface">
      <!-- Messages Area -->
      <div class="messages-container q-pa-md">
        <template v-if="messages.length">
          <div v-for="(message, index) in messages" :key="index">
            <!-- User Message -->
            <template v-if="message.type === 'user'">
              <q-chat-message
                :text="[message.content]"
                sent
                bg-color="primary"
                text-color="white"
              />
            </template>

            <!-- Bot Message or Error -->
            <template v-if="message.type === 'bot'">
              <!-- Fact Check Details -->
              <template v-if="message.verification">
                <q-card flat bordered class="q-mt-sm q-mb-md">
                  <!-- Classification Chip -->
                  <q-card-section>
                    <div class="row items-center q-gutter-sm">
                      <q-chip 
                        :color="getVerificationColor(message.verification.classification)"
                        text-color="white"
                        icon="fact_check"
                      >
                        {{ message.verification.classification }}
                      </q-chip>
                    </div>
                  </q-card-section>

                  <!-- Explanation -->
                  <q-card-section v-if="message.verification.explanation">
                    <div class="text-subtitle2">Explanation:</div>
                    <div class="text-body2">
                      {{ message.verification.explanation }}
                    </div>
                    <div class="row items-center q-gutter-sm q-mt-sm">
                      <q-chip 
                        clickable
                        icon="translate"
                        color="info"
                        text-color="white"
                        @click="showTranslateMenu($event, message.verification.explanation)"
                      >
                        Translate
                        <q-tooltip>
                          Translate this explanation to another language
                        </q-tooltip>
                      </q-chip>
                    </div>
                  </q-card-section>

                  <!-- Supporting Fragments -->
                  <q-card-section v-if="message.verification.fragments && message.verification.fragments.length">
                    <div class="text-subtitle2">Supporting Evidence:</div>
                    <q-list dense>
                      <q-item 
                        v-for="(fragment, idx) in message.verification.fragments" 
                        :key="idx"
                        class="q-pa-xs"
                      >
                        <q-item-section>
                          <q-item-label caption>
                            <q-icon name="arrow_right" size="xs" class="q-mr-xs" />
                            {{ fragment }}
                          </q-item-label>
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </q-card-section>

                  <!-- Sources -->
                  <q-card-section v-if="message.verification.sources">
                    <div class="text-subtitle2">Sources:</div>
                    <div class="q-gutter-sm">
                      <div v-for="(isVerified, source) in message.verification.sources" :key="source" class="inline-block">
                        <q-chip 
                          :color="isVerified ? 'positive' : 'warning'"
                          :text-color="isVerified ? 'white' : 'black'"
                          :icon="isVerified ? 'source' : 'error'"
                          :disable="!isVerified"
                          @click="showLanguageMenu(source, isVerified, $event)"
                        >
                          {{ source }}
                          <q-tooltip>
                            {{ isVerified ? 'Click to generate summary' : 'Unverified Source' }}
                          </q-tooltip>
                        </q-chip>

                        <q-menu v-model="sourceMenus[source]" :target="menuTargets[source]">
                          <q-card style="min-width: 250px">
                            <q-card-section>
                              <div class="text-h6">Generate Summary</div>
                              <div class="text-caption">Select language for {{ source }}</div>
                            </q-card-section>

                            <q-card-section class="q-pt-none">
                              <q-select
                                v-model="selectedLanguages[source]"
                                :options="languageOptions"
                                label="Language"
                                outlined
                                dense
                              />
                            </q-card-section>

                            <q-card-actions align="right">
                              <q-btn 
                                flat 
                                label="Cancel" 
                                color="negative" 
                                v-close-popup 
                              />
                              <q-btn 
                                flat 
                                label="Generate" 
                                color="primary"
                                @click="generateSummary(source)"
                                :loading="summaryLoading[source]"
                                :disable="!selectedLanguages[source]"
                              />
                            </q-card-actions>
                          </q-card>
                        </q-menu>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </template>

              <!-- Error Handling -->
              <template v-else-if="message.error">
                <q-card flat bordered class="q-mt-sm q-mb-md bg-negative text-white">
                  <q-card-section>
                    <div class="row items-center">
                      <q-icon name="error" size="md" class="q-mr-md" />
                      <div>
                        <div class="text-subtitle1">Error Processing Request</div>
                        <div class="text-body2">{{ message.content }}</div>
                      </div>
                    </div>
                  </q-card-section>
                  
                  <!-- Retry Button -->
                  <q-card-actions align="right">
                    <q-btn 
                      flat 
                      label="Retry" 
                      @click="retryLastMessage"
                      :disable="loading"
                    />
                  </q-card-actions>
                </q-card>
              </template>
            </template>
          </div>
        </template>
        <div v-else class="text-center text-grey q-pa-lg">
          <q-icon name="chat" size="4rem" />
          <div class="text-h6 q-mt-md">Start a conversation</div>
          <div class="text-body1">Enter a statement to verify its accuracy</div>
        </div>
      </div>

      <!-- Summary Dialog -->
      <q-dialog v-model="summaryDialog">
        <q-card style="min-width: 350px; max-width: 600px">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Summary</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <div class="text-subtitle2">{{ summaryInfo.source }}</div>
            <div class="text-caption">Translated to {{ summaryInfo.language }}</div>
            <q-separator class="q-my-md" />
            <div class="text-body1" style="white-space: pre-line">{{ summaryInfo.text }}</div>
          </q-card-section>
        </q-card>
      </q-dialog>

      <!-- Translation Menu -->
      <q-menu v-model="translateMenu.show" :target="translateMenu.target">
        <q-card style="min-width: 250px">
          <q-card-section>
            <div class="text-h6">Translate Explanation</div>
            <div class="text-caption">Select target language</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-select
              v-model="translateMenu.language"
              :options="languageOptions"
              label="Language"
              outlined
              dense
            />
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancel" color="negative" v-close-popup />
            <q-btn 
              flat 
              label="Translate" 
              color="primary"
              @click="translateExplanation(translateMenu.textToTranslate)"
              :loading="translateMenu.loading"
              :disable="!translateMenu.language"
            />
          </q-card-actions>
        </q-card>
      </q-menu>

      <!-- Input Area -->
      <div class="input-container q-px-md q-pb-md">
        <div class="row q-gutter-sm">
          <q-input
            v-model="newMessage"
            placeholder="Enter a statement to verify..."
            outlined
            rounded
            class="col"
            :disable="loading"
            hide-bottom-space
            bg-color="white"
            @keyup.enter="sendMessage"
          >
            <template v-slot:append>
              <q-btn
                round
                dense
                flat
                icon="send"
                :loading="loading"
                @click="sendMessage"
              />
            </template>
          </q-input>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      messages: [],
      newMessage: '',
      loading: false,
      lastUserMessage: null,
      sourceMenus: {},
      menuTargets: {},
      selectedLanguages: {},
      summaryLoading: {},
      summaryDialog: false,
      summaryInfo: {
        source: '',
        language: '',
        text: ''
      },
      translateMenu: {
        show: false,
        target: null,
        language: null,
        loading: false,
        textToTranslate: ''
      },
      languageOptions: [
        'English',
        'Spanish',
        'French',
        'German',
        'Italian',
        'Portuguese',
        'Chinese',
        'Japanese',
        'Korean',
        'Arabic',
        'Russian'
      ]
    };
  },
  methods: {
    async sendMessage() {
      if (!this.newMessage.trim() || this.loading) return;

      const messageText = this.newMessage;
      this.newMessage = '';
      this.lastUserMessage = messageText;

      // Add user message
      this.messages.push({
        type: 'user',
        content: messageText
      });

      this.loading = true;
      try {
        const response = await fetch('/api/fact-check', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ statement: messageText })
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText || 'Network response was not ok');
        }
        
        const result = await response.json();
        this.messages.push({
          type: 'bot',
          content: result.explanation || 'Fact checking complete',
          verification: result
        });
      } catch (error) {
        console.error('Error:', error);
        this.messages.push({
          type: 'bot',
          content: error.message || 'Unexpected error occurred. Please try again.',
          error: true
        });
      } finally {
        this.loading = false;
      }
    },
    showLanguageMenu(source, isVerified, event) {
      if (!isVerified) return;
      
      // Store the click event target for menu positioning
      this.menuTargets[source] = event.target;
      // Show the menu for this source
      this.sourceMenus[source] = true;
    },
    async generateSummary(source) {
      if (!this.selectedLanguages[source]) return;

      this.summaryLoading = { ...this.summaryLoading, [source]: true };
      
      try {
        const response = await fetch('/api/summarize-source', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            source: source,
            target_language: this.selectedLanguages[source]
          })
        });

        if (!response.ok) {
          throw new Error('Failed to generate summary');
        }

        const result = await response.json();
        
        // Show summary in dialog
        this.summaryInfo = {
          source: result.source,
          language: result.target_language,
          text: result.summary
        };
        this.summaryDialog = true;

        // Close the language menu
        this.sourceMenus[source] = false;
        
      } catch (error) {
        console.error('Summary generation error:', error);
        this.$q.notify({
          type: 'negative',
          message: 'Failed to generate summary'
        });
      } finally {
        this.summaryLoading = { ...this.summaryLoading, [source]: false };
      }
    },
    showTranslateMenu(event, text) {
      this.translateMenu.target = event.target;
      this.translateMenu.textToTranslate = text;
      this.translateMenu.show = true;
    },
    async translateExplanation(text) {
      if (!this.translateMenu.language) return;

      this.translateMenu.loading = true;
      
      try {
        const response = await fetch('/api/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            text: text,
            target_language: this.translateMenu.language
          })
        });

        if (!response.ok) {
          throw new Error('Failed to translate text');
        }

        const result = await response.json();
        
        // Show translation in dialog
        this.summaryInfo = {
          source: 'Explanation',
          language: result.target_language,
          text: result.translated_text
        };
        this.summaryDialog = true;

        // Close the translate menu
        this.translateMenu.show = false;
        
      } catch (error) {
        console.error('Translation error:', error);
        this.$q.notify({
          type: 'negative',
          message: 'Failed to translate text'
        });
      } finally {
        this.translateMenu.loading = false;
      }
    },
    retryLastMessage() {
      if (this.lastUserMessage) {
        this.newMessage = this.lastUserMessage;
        this.sendMessage();
      }
    },
    getVerificationColor(classification) {
      const colors = {
        'TRUE': 'positive',
        'FALSE': 'negative',
        'PARTIALLY TRUE': 'warning',
        'NOT ENOUGH INFORMATION': 'grey'
      };
      return colors[classification.toUpperCase()] || 'grey';
    }
  }
};

export default ChatInterface;