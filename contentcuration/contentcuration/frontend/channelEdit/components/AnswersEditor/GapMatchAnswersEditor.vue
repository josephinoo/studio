<template>
  <div>
    <div class="grey--text mb-3 text--darken-1">
      Gap Match Choices
    </div>
    <div class="mb-3">
      Use the format <code>[gap_id]</code> in the Question text where you want blanks. Provide the valid choices here and map them to the gaps.
    </div>
    <div>
      <div v-if="!choices || !choices.length" class="card-border-light pa-3">
        No choices available.
      </div>
      <div
        v-for="(choice, choiceIdx) in choices"
        :key="choiceIdx"
        class="card-border-light"
      >
        <VCard class="answer editable" flat data-test="answer">
          <VCardText>
            <VLayout align-top>
              <VFlex xs6>
                <div class="grey--text mb-1">Choice Text</div>
                <TipTapEditor
                  v-model="choice.answer"
                  class="editor"
                  mode="edit"
                  :imageProcessor="EditorImageProcessor"
                  @update="updateChoiceText($event, choiceIdx)"
                />
              </VFlex>
              <VFlex xs5 class="pl-3">
                <div class="grey--text mb-1">Target Gap Identifier (e.g. gap_1)</div>
                <VTextField
                  :value="getGapMapping(choice.id)"
                  placeholder="gap_1"
                  @change="updateMapping(choice.id, $event)"
                />
              </VFlex>
              <VSpacer />
              <VFlex shrink>
                <AssessmentItemToolbar
                  :iconActionsConfig="toolbarIconActions"
                  :canMoveUp="false"
                  :canMoveDown="false"
                  class="toolbar"
                  analyticsLabel="Choice"
                  data-test="toolbar"
                  @click="onToolbarClick($event, choiceIdx)"
                />
              </VFlex>
            </VLayout>
          </VCardText>
        </VCard>
      </div>
    </div>
    <KButton
      text="New choice"
      class="ml-0 mt-3"
      data-test="newAnswerBtn"
      @click="addNewChoice"
    />
  </div>
</template>

<script>
  import AssessmentItemToolbar from '../AssessmentItemToolbar';
  import { AssessmentItemToolbarActions } from '../../constants';
  import EditorImageProcessor from 'shared/views/TipTapEditor/TipTapEditor/services/imageService';
  import TipTapEditor from 'shared/views/TipTapEditor/TipTapEditor/TipTapEditor.vue';

  function generateId() {
    return Math.random().toString(36).substring(2, 10);
  }

  export default {
    name: 'GapMatchAnswersEditor',
    components: {
      AssessmentItemToolbar,
      TipTapEditor,
    },
    model: {
      prop: 'answers',
      event: 'update',
    },
    props: {
      answers: {
        type: [Array, Object],
        default: () => ({ choices: [], correctMapping: {} }),
      },
    },
    data() {
      return {
        EditorImageProcessor,
        toolbarIconActions: [
          AssessmentItemToolbarActions.DELETE_ITEM,
        ],
      };
    },
    computed: {
      choices() {
        if (Array.isArray(this.answers)) {
          return this.answers;
        }
        return this.answers.choices || [];
      },
      mapping() {
        if (Array.isArray(this.answers)) {
          return {};
        }
        return this.answers.correctMapping || {};
      }
    },
    methods: {
      emitUpdate(updatedData) {
        this.$emit('update', updatedData);
      },
      getGapMapping(choiceId) {
        // Find mapping: gap_Id -> choiceId
        for (const [gapId, mappedChoiceId] of Object.entries(this.mapping)) {
           if (mappedChoiceId === choiceId) return gapId;
        }
        return '';
      },
      updateMapping(choiceId, gapIdText) {
        const currentMapping = { ...this.mapping };
        // Remove existing mapping for this choice
        for (const [key, val] of Object.entries(currentMapping)) {
            if (val === choiceId) delete currentMapping[key];
        }
        if (gapIdText && gapIdText.trim()) {
           currentMapping[gapIdText.trim()] = choiceId;
        }
        this.emitUpdate({ choices: this.choices, correctMapping: currentMapping });
      },
      deleteChoice(choiceIdx) {
        const choiceToDelete = this.choices[choiceIdx];
        const updatedChoices = [...this.choices];
        updatedChoices.splice(choiceIdx, 1);
        
        const updatedMapping = { ...this.mapping };
        for (const [key, val] of Object.entries(updatedMapping)) {
            if (val === choiceToDelete.id) delete updatedMapping[key];
        }
        
        this.emitUpdate({ choices: updatedChoices, correctMapping: updatedMapping });
      },
      onToolbarClick(action, choiceIdx) {
        if (action === AssessmentItemToolbarActions.DELETE_ITEM) {
          this.deleteChoice(choiceIdx);
        }
      },
      updateChoiceText(newText, choiceIdx) {
        const updatedChoices = [...this.choices];
        updatedChoices[choiceIdx].answer = newText;
        this.emitUpdate({ choices: updatedChoices, correctMapping: this.mapping });
      },
      addNewChoice() {
        const updatedChoices = [...this.choices];
        updatedChoices.push({
          answer: '',
          id: `choice_${generateId()}`,
        });
        this.emitUpdate({ choices: updatedChoices, correctMapping: this.mapping });
      },
    },
  };
</script>

<style lang="scss" scoped>
  .card-border-light {
    /* stylelint-disable-next-line custom-property-pattern */
    border: 1px solid var(--v-greyBorder-lighten1);

    &:not(:first-child) {
      border-top: 0;
    }
  }

  .answer {
    position: relative;
  }
</style>
