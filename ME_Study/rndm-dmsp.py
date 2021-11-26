 
import pandas as pd
import numpy as np
import re
import time

stimuli = pd.read_csv('stimuli-dmsp.csv')

##########################
# Stage 1 - Select Verbs #
##########################

def select_verbs(speaker):
   familiar_dialect = 'AAE' if speaker == 'aae' else 'GAE' # Set dialect markers
   unfamiliar_dialect = 'GAE' if speaker == 'aae' else 'AAE'
   stimuli['Speaker'] = unfamiliar_dialect # Create Speaker column and set to unfamiliar

   pred_verbs = stimuli[stimuli['Verb_Type'] == 'Predictive'] # Select Predictive Verbs
   pred_verbs_18 = pred_verbs.iloc[np.random.choice(pred_verbs.shape[0], 18, replace = False)] # Randomly choose 18 (all)
   pred_verbs_opt = pred_verbs_18[:9].copy() # Split into Optimal and Suboptimal
   pred_verbs_sub = pred_verbs_18[9:].copy()
   num_from_opt = np.random.randint(3, 7) # Choose at a number of verbs to take from Optimal for Intermediate (>= 3 and <= 6)
   pred_verbs_int_opt = pred_verbs_opt.iloc[np.random.choice(pred_verbs_opt.shape[0], num_from_opt, replace = False)] # Randomly choose from Optimal verbs
   pred_verbs_int_sub = pred_verbs_sub.iloc[np.random.choice(pred_verbs_sub.shape[0], 9 - num_from_opt, replace = False)] # Randomly choose the rest from Suboptimal verbs
   pred_verbs_int = pd.concat([pred_verbs_int_opt, pred_verbs_int_sub]) # Concatenate into full Intermediate
   pred_verbs_opt['Verb-NounAudio'] = pred_verbs_opt['Verb-NounAudio'].str[:-4] + '_' + familiar_dialect + pred_verbs_opt['Verb-NounAudio'].str[-4:] # Splice in dialect markers
   pred_verbs_sub['Verb-NounAudio'] = pred_verbs_sub['Verb-NounAudio'].str[:-4] + '_' + unfamiliar_dialect + pred_verbs_sub['Verb-NounAudio'].str[-4:]
   pred_verbs_int['Verb-NounAudio'] = pred_verbs_int['Verb-NounAudio'].str[:-4] + '_' + unfamiliar_dialect + pred_verbs_int['Verb-NounAudio'].str[-4:]
   pred_verbs_opt['Speaker'] = familiar_dialect # Set the optimal speakers to the familiar dialect

   neut_fillers = stimuli[stimuli['Verb_Type'] == 'NeutralFiller'] # Select Neutral Fillers
   neut_fillers_opt = neut_fillers[neut_fillers['Target Object'].isin(pred_verbs_opt['Target Object'])] # Remove targets not selected earlier
   neut_fillers_opt = neut_fillers_opt.iloc[np.random.choice(neut_fillers_opt.shape[0], 3, replace = False)] # Randomly choose 3
   neut_fillers_opt['Verb-NounAudio'] = neut_fillers_opt['Verb-NounAudio'].str[:-4] + '_' + familiar_dialect + neut_fillers_opt['Verb-NounAudio'].str[-4:] # Splice in dialect markers
   neut_fillers_opt['Speaker'] = familiar_dialect # Set the optimal speakers to the familiar dialect
   neut_fillers_sub = neut_fillers[neut_fillers['Target Object'].isin(pred_verbs_sub['Target Object'])] # Repeat for other conditions (except setting speaker)
   neut_fillers_sub = neut_fillers_sub.iloc[np.random.choice(neut_fillers_sub.shape[0], 3, replace = False)]
   neut_fillers_sub['Verb-NounAudio'] = neut_fillers_sub['Verb-NounAudio'].str[:-4] + '_' + unfamiliar_dialect + neut_fillers_sub['Verb-NounAudio'].str[-4:]
   neut_fillers_int = neut_fillers[neut_fillers['Target Object'].isin(pred_verbs_int['Target Object'])]
   neut_fillers_int = neut_fillers_int.iloc[np.random.choice(neut_fillers_int.shape[0], 3, replace = False)]
   neut_fillers_int['Verb-NounAudio'] = neut_fillers_int['Verb-NounAudio'].str[:-4] + '_' + unfamiliar_dialect + neut_fillers_int['Verb-NounAudio'].str[-4:]

   fillers = stimuli[stimuli['Verb_Type'] == 'Filler'] # Select Neutral Fillers
   fillers_opt = fillers[fillers['Target Object'].isin(pred_verbs_opt['Unrelated Foil A']) | fillers['Target Object'].isin(pred_verbs_opt['Unrelated Foil B']) | fillers['Target Object'].isin(pred_verbs_opt['Unrelated Foil C'])] # Remove targets not selected in earlier image sets
   fillers_opt = fillers_opt.iloc[np.random.choice(fillers_opt.shape[0], 6, replace = False)] # Randomly choose 6
   fillers_opt['Verb-NounAudio'] = fillers_opt['Verb-NounAudio'].str[:-4] + '_' + familiar_dialect + fillers_opt['Verb-NounAudio'].str[-4:] # Splice in dialect markers
   fillers_opt['Speaker'] = familiar_dialect # Set the optimal speakers to the familiar dialect
   fillers_sub = fillers[fillers['Target Object'].isin(pred_verbs_sub['Unrelated Foil A']) | fillers['Target Object'].isin(pred_verbs_sub['Unrelated Foil B']) | fillers['Target Object'].isin(pred_verbs_sub['Unrelated Foil C'])] # Repeat for other conditions (except setting speaker)
   fillers_sub = fillers_sub.iloc[np.random.choice(fillers_sub.shape[0], 6, replace = False)]
   fillers_sub['Verb-NounAudio'] = fillers_sub['Verb-NounAudio'].str[:-4] + '_' + unfamiliar_dialect + fillers_sub['Verb-NounAudio'].str[-4:]
   fillers_int = fillers[fillers['Target Object'].isin(pred_verbs_int['Unrelated Foil A']) | fillers['Target Object'].isin(pred_verbs_int['Unrelated Foil B']) | fillers['Target Object'].isin(pred_verbs_int['Unrelated Foil C'])]
   fillers_int = fillers_int.iloc[np.random.choice(fillers_int.shape[0], 6, replace = False)]
   fillers_int['Verb-NounAudio'] = fillers_int['Verb-NounAudio'].str[:-4] + '_' + unfamiliar_dialect + fillers_int['Verb-NounAudio'].str[-4:]

   # Concat into one frame
   all_opt = pd.concat([pred_verbs_opt, neut_fillers_opt, fillers_opt])
   all_sub = pd.concat([pred_verbs_sub, neut_fillers_sub, fillers_sub])
   all_int = pd.concat([pred_verbs_int, neut_fillers_int, fillers_int])
   trials = pd.concat([all_opt, all_sub, all_int], keys = ['optimal', 'suboptimal', 'intermediate']) # Use multi-index to keep condition segregation

   # Reindex and make columns out of old indices
   trials.index = trials.index.set_names(['Condition', 'Original Index'])
   trials = trials.reset_index()

   return trials

######################
# Stage 2 - Intermix #
######################

def intermix(speaker):
   start_time = time.time()

   trials = select_verbs(speaker)

   meets_constraints = False
   while not meets_constraints:
      meets_constraints = True

      trials = trials.sample(frac = 1) # Shuffle

      # Ensure consecutive targets are different (so Predictive and Neutral verb pairs do not occur next to each other)
      targets = trials['Target Object'].to_numpy()
      for i in range(len(targets) - 1):
         if targets[i] == targets[i + 1]:
            meets_constraints = False
            break

      if meets_constraints:
         # Ensure image sets do not occur next to each other
         image_sets = trials[['Target Object', 'Unrelated Foil A', 'Unrelated Foil B', 'Unrelated Foil C']].to_numpy()
         for i in range(len(image_sets) - 1):
            if set(image_sets[i]) == set(image_sets[i + 1]):
               meets_constraints = False
               break
      
      if meets_constraints:
         # Ensure no more than 2 conditions in a row
         conditions = trials['Condition'].to_numpy()
         for i in range(len(conditions) - 2):
            if conditions[i] == conditions[i + 1] and conditions[i] == conditions[i + 2]:
               meets_constraints = False
               break 

      if meets_constraints:
         # Ensure one image cannot show up more than 10 times total
         all_img_names = list(trials[['TargetImage', 'FoilAImage', 'FoilBImage', 'FoilCImage']].to_numpy().flatten())
         if max([all_img_names.count(name) for name in all_img_names]) > 10:
            meets_constraints = False
      
      # Repick verbs if takes more than 2 seconds (not all combinations yield viable results)
      if time.time() - start_time > 2:
         start_time = time.time()
         trials = intermix(speaker)

   # Reindex to be in order (original indices are still preserved in a column)
   trials = trials.reset_index(drop = True)

   return trials

############################
# Assign Numbers to Images #
############################

def assign_numbers(trials):
   # Create image names with numbers
   all_img_names = list(trials[['TargetImage', 'FoilAImage', 'FoilBImage', 'FoilCImage']].to_numpy().flatten())
   all_img_names_cnt = {name: all_img_names.count(name) for name in all_img_names} # Create dict with the image number assignments
   all_img_num_names = []
   for name, cnt in all_img_names_cnt.items():
      no_consecutive_nums = False
      while not no_consecutive_nums:
         no_consecutive_nums = True

         # Generate numbers 1-4 in groups of 4
         nums = []
         for i in range(int(np.ceil(cnt / 4))):
            nums.extend(np.random.choice(range(1, 5), 4, replace = False))

         # Ensure there are no consecutive numbers so that the same images cannot appear consecutively
         for i in range(3, len(nums) - 1, 4): # Only need to check every 4th index
            if nums[i] == nums[i + 1]:
               no_consecutive_nums = False
               break

      # Splice in numbers to a list of image names
      for i in range(cnt):
         all_img_num_names += [name[:-4] + str(nums[i]) + name[-4:]]

   # Replace image names so that they have numbers, using the randomized order generated above
   for i in range(trials.shape[0]):
      txt = ' ' + ' '.join(all_img_num_names) # join togther into list with spaces for searching; need to search with space at beginning b/c some words are subsets (ie. ball and football)

      r = re.search(' ' + trials.loc[i, 'Target Object'] + '\d\.\w{3}', txt) # Match the first instance of target image
      trials.loc[i, 'TargetImage'] = r.group(0)[1:] # Replace with the new name (that has the assigned number) after splicing off leading space
      all_img_num_names.remove(r.group(0)[1:]) # Remove the first instance from the generated names so that next time, the "second" match will be used; splice off leading space
      
      r = re.search(' ' + trials.loc[i, 'Unrelated Foil A'] + '\d\.\w{3}', txt) # Repeat for the 3 foils in each image set
      trials.loc[i, 'FoilAImage'] = r.group(0)[1:]
      all_img_num_names.remove(r.group(0)[1:])
         
      r = re.search(' ' + trials.loc[i, 'Unrelated Foil B'] + '\d\.\w{3}', txt)
      trials.loc[i, 'FoilBImage'] = r.group(0)[1:]
      all_img_num_names.remove(r.group(0)[1:])
         
      r = re.search(' ' + trials.loc[i, 'Unrelated Foil C'] + '\d\.\w{3}', txt)
      trials.loc[i, 'FoilCImage'] = r.group(0)[1:]
      all_img_num_names.remove(r.group(0)[1:])
   
   return trials

for i in range(5):
   print('aae' + str(i))
   assign_numbers(intermix('aae')).to_csv('/home/sam/Documents/ME_Study/randomized_stimuli_dmsp/randomized_stimuli_AAE' + str(i) + '.csv', index = False) # Export to csv
   print('gae' + str(i))
   assign_numbers(intermix('gae')).to_csv('/home/sam/Documents/ME_Study/randomized_stimuli_dmsp/randomized_stimuli_GAE' + str(i) + '.csv', index = False)
