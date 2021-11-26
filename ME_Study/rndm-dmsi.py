import pandas as pd
import numpy as np
import re
import time

stimuli = pd.read_csv('stimuli-dmsi.csv')

##########################
# Stage 1 - Select Verbs #
##########################

def select_verbs(speaker):
   familiar_dialect = 'AAE' if speaker == 'aae' else 'GAE' # Set dialect markers
   unfamiliar_dialect = 'GAE' if speaker == 'aae' else 'AAE'
   stimuli['Speaker'] = unfamiliar_dialect # Create Speaker column and set to unfamiliar

   some_trials = stimuli[stimuli['Trial_type'] == 'some'] # Select Predictive Verbs
   some_trials = some_trials.sample(frac = 1) # Randomly shuffle
   some_trials_opt = some_trials[:4].copy() # Split into Optimal, Suboptimal, and Intermediate
   some_trials_sub = some_trials[4:8].copy()
   some_trials_int = some_trials[8:].copy()
   some_trials_opt['critical_audio'] = some_trials_opt['critical_audio'].str[:-4] + '_' + familiar_dialect + some_trials_opt['critical_audio'].str[-4:] # Splice in dialect markers
   some_trials_sub['critical_audio'] = some_trials_sub['critical_audio'].str[:-4] + '_' + unfamiliar_dialect + some_trials_sub['critical_audio'].str[-4:]
   some_trials_int['critical_audio'] = some_trials_int['critical_audio'].str[:-4] + '_' + unfamiliar_dialect + some_trials_int['critical_audio'].str[-4:]
   some_trials_opt['Speaker'] = familiar_dialect # Set the optimal speakers to the familiar dialect

   filler_allh = stimuli[stimuli['Trial_type'] == 'filler_allh'] # Select Homophonous filler_allnh
   duped_filler_allh = filler_allh.iloc[np.random.choice(filler_allh.shape[0], 2, replace = False)]
   duped_filler_allh.index = [26, 27]
   filler_allh_opt = filler_allh[:2].copy() # Split into Optimal, Suboptimal, and Intermediate
   filler_allh_sub = filler_allh[2:].copy()
   filler_allh_int = duped_filler_allh.copy()
   filler_allh_opt['critical_audio'] = filler_allh_opt['critical_audio'].str[:-4] + '_' + familiar_dialect + filler_allh_opt['critical_audio'].str[-4:] # Splice in dialect markers
   filler_allh_int['critical_audio'] = filler_allh_int['critical_audio'].str[:-4] + '_' + unfamiliar_dialect + filler_allh_int['critical_audio'].str[-4:]
   filler_allh_sub['critical_audio'] = filler_allh_sub['critical_audio'].str[:-4] + '_' + unfamiliar_dialect + filler_allh_sub['critical_audio'].str[-4:] 
   filler_allh_opt['Speaker'] = familiar_dialect # Set the optimal speakers to the familiar dialect

   filler_allnh = stimuli[stimuli['Trial_type'] == 'filler_allnh'] # Select Homophonous filler_allnh
   filler_allnh = filler_allnh.sample(frac = 1) # Randomly shuffle
   filler_allnh_opt = filler_allnh[:3].copy() # Split into Optimal, Suboptimal, and Intermediate
   filler_allnh_sub = filler_allnh[3:6].copy()
   filler_allnh_int = filler_allnh[6:].copy()
   filler_allnh_opt['critical_audio'] = filler_allnh_opt['critical_audio'].str[:-4] + '_' + familiar_dialect + filler_allnh_opt['critical_audio'].str[-4:] # Splice in dialect markers
   filler_allnh_int['critical_audio'] = filler_allnh_int['critical_audio'].str[:-4] + '_' + unfamiliar_dialect + filler_allnh_int['critical_audio'].str[-4:]
   filler_allnh_sub['critical_audio'] = filler_allnh_sub['critical_audio'].str[:-4] + '_' + unfamiliar_dialect + filler_allnh_sub['critical_audio'].str[-4:] 
   filler_allnh_opt['Speaker'] = familiar_dialect # Set the optimal speakers to the familiar dialect

   # Concat into one frame
   all_opt = pd.concat([some_trials_opt, filler_allh_opt, filler_allnh_opt])
   all_sub = pd.concat([some_trials_sub, filler_allh_sub, filler_allnh_sub])
   all_int = pd.concat([some_trials_int, filler_allh_int, filler_allnh_int])
   trials = pd.concat([all_opt, all_sub, all_int], keys = ['optimal', 'suboptimal', 'intermediate']) # Use multi-index to keep condition segregation

   # Reindex and make columns out of old indices
   trials.index = trials.index.set_names(['Condition', 'Original Index'])
   trials = trials.reset_index()

   return trials

######################
# Stage 2 - Intermix #
######################

def intermix(speaker):
   trials = select_verbs(speaker)

   meets_constraints = False
   while not meets_constraints:
      meets_constraints = True

      trials = trials.sample(frac = 1) # Shuffle

      # Ensure consecutive trial types are different
      trial_types = trials['Trial_type'].to_numpy()
      for i in range(len(trial_types) - 3):
         if trial_types[i] == trial_types[i + 1] and trial_types[i + 1] == trial_types[i + 2]:
            meets_constraints = False
            break
      
      if meets_constraints:
         # Ensure no more than 2 conditions in a row
         conditions = trials['Condition'].to_numpy()
         for i in range(len(conditions) - 2):
            if conditions[i] == conditions[i + 1] and conditions[i] == conditions[i + 2]:
               meets_constraints = False
               break 

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
   intermix('aae').to_csv('/home/sam/Documents/ME_Study/randomized_stimuli_dmsi/randomized_stimuli_AAE' + str(i) + '.csv', index = False) # Export to csv
   print('gae' + str(i))
   intermix('gae').to_csv('/home/sam/Documents/ME_Study/randomized_stimuli_dmsi/randomized_stimuli_GAE' + str(i) + '.csv', index = False)
